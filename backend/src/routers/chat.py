"""
Chat router with SSE streaming support.
Updated for Better Auth JWT authentication.
"""

import json
import logging
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from agents import Runner

from ..schemas.chat import ChatRequest, ChatStreamDelta, ChatStreamDone, ChatStreamError, Citation
from ..chatbot.agent import create_textbook_agent
from ..chatbot.context import ChatbotRunContext
from ..middleware.jwt_auth import get_current_user
from ..models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


async def generate_chat_stream(request: ChatRequest) -> AsyncGenerator[str, None]:
    """
    Generate SSE stream for chat response.

    Args:
        request: Chat request with message and context

    Yields:
        SSE-formatted events (delta, citation, done, error)
    """
    try:
        # Create run context
        run_context = ChatbotRunContext()
        run_context.selected_text = request.selected_text
        run_context.quick_action = request.quick_action

        # Create agent with context
        agent = create_textbook_agent(
            selected_text=request.selected_text,
            quick_action=request.quick_action
        )

        # Build input list from conversation history + current message
        input_items = []

        # Add conversation history (limited to last 10 messages)
        if request.conversation_history:
            for msg in request.conversation_history[-10:]:
                input_items.append({
                    "role": msg.role,
                    "content": msg.content
                })

        # Add current user message
        user_message = request.message
        if request.selected_text:
            user_message = f"[Selected text: {request.selected_text}]\n\n{user_message}"

        input_items.append({
            "role": "user",
            "content": user_message
        })

        # Run agent with streaming using correct API parameters
        result = Runner.run_streamed(
            starting_agent=agent,
            input=input_items,
            context=run_context,
        )

        # Track whether we're currently streaming tool call arguments
        streaming_tool_call = False
        
        # Stream events and filter appropriately
        async for event in result.stream_events():
            event_type = getattr(event, 'type', None)
            
            if event_type == "run_item_stream_event":
                # Track item types to know when tool calls start/end
                item = getattr(event, 'item', None)
                if item:
                    item_type = getattr(item, 'type', None)
                    if item_type == "function_call_item":
                        streaming_tool_call = True
                    elif item_type == "message_output_item":
                        streaming_tool_call = False
                        
            elif event_type == "raw_response_event":
                # Skip if we're in a tool call
                if streaming_tool_call:
                    continue
                    
                data = event.data
                data_type = getattr(data, 'type', None)
                
                # Only emit content deltas, not function call deltas
                if data_type and 'function' in str(data_type):
                    continue
                    
                # Get delta text
                delta = getattr(data, 'delta', None)
                if delta:
                    delta_event = ChatStreamDelta(content=delta)
                    yield f"data: {delta_event.model_dump_json()}\n\n"
                    
            elif event_type == "agent_updated_stream_event":
                # Agent handoff - reset tool call state
                streaming_tool_call = False

        # Send citations at the end
        citations = [
            Citation(
                chapter=c.chapter,
                section=c.section,
                title=c.title,
                url=c.url,
                relevance_score=c.relevance_score,
                snippet=c.snippet
            )
            for c in run_context.citations
        ]

        done_event = ChatStreamDone(citations=citations)
        yield f"data: {done_event.model_dump_json()}\n\n"

    except Exception as e:
        logger.error(f"Error during chat streaming: {e}", exc_info=True)
        error_event = ChatStreamError(
            message=str(e),
            code="STREAM_ERROR"
        )
        yield f"data: {error_event.model_dump_json()}\n\n"


@router.post("")
async def chat(
    request: ChatRequest,
    user: User = Depends(get_current_user)
):
    """
    Chat endpoint with Server-Sent Events (SSE) streaming.

    **Requires authentication via Bearer token.**

    Accepts a user message and optional conversation history, then streams
    the AI response token-by-token along with citations.

    Args:
        request: ChatRequest with message and context
        user: Authenticated user from JWT token

    Returns:
        StreamingResponse with SSE events

    Raises:
        HTTPException: 401 if not authenticated
    """
    logger.info(f"Chat request from user {user.id} ({user.email})")

    return StreamingResponse(
        generate_chat_stream(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
    )


@router.get("/health")
async def health():
    """Health check endpoint for the chat service."""
    return {"status": "healthy", "service": "chatbot"}
