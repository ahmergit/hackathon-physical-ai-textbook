"""
Pydantic schemas for chat API.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, List


class ConversationMessage(BaseModel):
    """A single message in the conversation history."""
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """Request payload for the chat endpoint."""
    message: str = Field(..., min_length=1, max_length=5000, description="User's question or query")
    conversation_history: List[ConversationMessage] = Field(
        default_factory=list,
        description="Previous messages for context (max 50)",
        max_length=50
    )
    selected_text: Optional[str] = Field(
        None,
        max_length=5000,
        description="Text selected from textbook page"
    )
    quick_action: Optional[Literal["explain", "summarize", "simplify"]] = Field(
        None,
        description="Quick action to apply to the response"
    )


class Citation(BaseModel):
    """Citation reference to textbook content."""
    chapter: str
    section: str
    title: str
    url: str
    relevance_score: float
    snippet: Optional[str] = None


class ChatStreamDelta(BaseModel):
    """Streaming delta event."""
    type: Literal["delta"] = "delta"
    content: str


class ChatStreamCitation(BaseModel):
    """Citation event during streaming."""
    type: Literal["citation"] = "citation"
    citation: Citation


class ChatStreamDone(BaseModel):
    """Stream completion event."""
    type: Literal["done"] = "done"
    citations: List[Citation]


class ChatStreamError(BaseModel):
    """Error event during streaming."""
    type: Literal["error"] = "error"
    message: str
    code: str
