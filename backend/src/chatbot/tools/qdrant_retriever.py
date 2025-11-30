"""
Qdrant retriever tool for OpenAI Agents SDK.
Searches the textbook vector database and returns relevant chunks.
"""

from typing import List
from datetime import datetime
from uuid import UUID

from agents import function_tool, RunContextWrapper
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, ScoredPoint

from ...config import settings
from ...services.embedding_service import embedding_service
from ..models import TextbookChunk
from ..context import ChatbotRunContext


# Initialize Qdrant client
qdrant_client = AsyncQdrantClient(
    url=settings.qdrant_url,
    api_key=settings.qdrant_api_key if settings.qdrant_api_key else None,
)


@function_tool
async def search_textbook(ctx: RunContextWrapper[ChatbotRunContext], query: str, top_k: int = 3) -> str:
    """
    Search the Physical AI textbook for relevant content.

    This tool performs semantic search over the textbook content using vector embeddings.
    Use this tool to find relevant information from the textbook to answer user questions.

    Args:
        query: The search query or question
        top_k: Number of results to return (default: 3)

    Returns:
        Formatted string with relevant textbook content and citations
    """
    # Get run context
    run_context: ChatbotRunContext = ctx.context

    # Generate query embedding
    query_embedding = await embedding_service.generate_embedding(query)

    # Search Qdrant
    search_response = await qdrant_client.query_points(
        collection_name=settings.qdrant_collection,
        query=query_embedding,
        limit=top_k,
        with_payload=True,
        score_threshold=0.3,  # Lowered threshold to get more results
    )
    search_results = search_response.points

    if not search_results:
        return "No relevant content found in the textbook for this query. Try rephrasing your question."

    # Convert results to TextbookChunk objects
    chunks = []
    scores = []

    for result in search_results:
        payload = result.payload

        # Handle ID - might be string or UUID
        chunk_id = result.id if isinstance(result.id, UUID) else UUID(str(result.id))

        chunk = TextbookChunk(
            id=chunk_id,
            content=payload["content"],
            chapter=payload["chapter"],
            chapter_title=payload["chapter_title"],
            section=payload["section"],
            section_title=payload["section_title"],
            page_path=payload["page_path"],  # Already includes anchor from ingestion
            chunk_index=payload["chunk_index"],
            token_count=payload["token_count"],
            created_at=datetime.fromisoformat(payload["created_at"]),
            heading=payload.get("heading"),  # Section heading if available
            anchor=payload.get("anchor"),    # URL anchor fragment
        )

        chunks.append(chunk)
        scores.append(result.score)

    # Store in context for citation generation
    run_context.add_retrieval_result(chunks, scores)

    # Return formatted context for the LLM
    return run_context.get_context_string()


@function_tool
async def search_textbook_by_chapter(ctx: RunContextWrapper[ChatbotRunContext], chapter: str, query: str, top_k: int = 3) -> str:
    """
    Search within a specific chapter of the textbook.

    Use this when the user asks about a specific chapter or you need to narrow results
    to a particular section of the textbook.

    Args:
        chapter: Chapter identifier (e.g., "chapter-01")
        query: The search query
        top_k: Number of results to return (default: 3)

    Returns:
        Formatted string with relevant content from the specified chapter
    """
    # Get run context
    run_context: ChatbotRunContext = ctx.context

    # Generate query embedding
    query_embedding = await embedding_service.generate_embedding(query)

    # Search with chapter filter
    search_response = await qdrant_client.query_points(
        collection_name=settings.qdrant_collection,
        query=query_embedding,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="chapter",
                    match=MatchValue(value=chapter)
                )
            ]
        ),
        limit=top_k,
        with_payload=True,
        score_threshold=0.3,  # Lowered threshold
    )
    search_results = search_response.points

    if not search_results:
        return f"No relevant content found in {chapter} for this query."

    # Convert results to TextbookChunk objects
    chunks = []
    scores = []

    for result in search_results:
        payload = result.payload

        # Handle ID - might be string or UUID
        chunk_id = result.id if isinstance(result.id, UUID) else UUID(str(result.id))

        chunk = TextbookChunk(
            id=chunk_id,
            content=payload["content"],
            chapter=payload["chapter"],
            chapter_title=payload["chapter_title"],
            section=payload["section"],
            section_title=payload["section_title"],
            page_path=payload["page_path"],  # Already includes anchor from ingestion
            chunk_index=payload["chunk_index"],
            token_count=payload["token_count"],
            created_at=datetime.fromisoformat(payload["created_at"]),
            heading=payload.get("heading"),  # Section heading if available
            anchor=payload.get("anchor"),    # URL anchor fragment
        )

        chunks.append(chunk)
        scores.append(result.score)

    # Store in context
    run_context.add_retrieval_result(chunks, scores)

    return run_context.get_context_string()
