"""
Unit tests for Qdrant retriever tool.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from datetime import datetime

from chatbot.tools.qdrant_retriever import search_textbook, search_textbook_by_chapter
from chatbot.context import ChatbotRunContext


@pytest.mark.asyncio
async def test_search_textbook_returns_relevant_chunks():
    """Test that search_textbook returns relevant chunks from Qdrant."""
    # Mock context
    ctx = MagicMock()
    ctx.context = ChatbotRunContext()

    # Mock Qdrant search results
    mock_result = MagicMock()
    mock_result.id = str(uuid4())
    mock_result.score = 0.85
    mock_result.payload = {
        "content": "Physical AI refers to artificial intelligence systems that interact with the physical world.",
        "chapter": "chapter-01",
        "chapter_title": "Introduction to Physical AI",
        "section": "section-1-1",
        "section_title": "What is Physical AI?",
        "page_path": "/docs/chapter-01/intro",
        "chunk_index": 0,
        "token_count": 128,
        "created_at": datetime.utcnow().isoformat(),
    }

    with patch('chatbot.tools.qdrant_retriever.qdrant_client') as mock_client:
        mock_client.search = AsyncMock(return_value=[mock_result])

        with patch('chatbot.tools.qdrant_retriever.embedding_service') as mock_embedding:
            mock_embedding.generate_embedding = AsyncMock(return_value=[0.1] * 1536)

            result = await search_textbook(ctx, query="What is Physical AI?")

            # Verify result contains context
            assert "Physical AI refers to" in result
            assert "Introduction to Physical AI" in result
            assert len(ctx.context.retrieved_chunks) == 1
            assert len(ctx.context.citations) == 1
            assert ctx.context.citations[0].relevance_score == 0.85


@pytest.mark.asyncio
async def test_search_textbook_handles_no_results():
    """Test that search_textbook handles empty results gracefully."""
    ctx = MagicMock()
    ctx.context = ChatbotRunContext()

    with patch('chatbot.tools.qdrant_retriever.qdrant_client') as mock_client:
        mock_client.search = AsyncMock(return_value=[])

        with patch('chatbot.tools.qdrant_retriever.embedding_service') as mock_embedding:
            mock_embedding.generate_embedding = AsyncMock(return_value=[0.1] * 1536)

            result = await search_textbook(ctx, query="irrelevant query")

            assert "No relevant content found" in result
            assert len(ctx.context.retrieved_chunks) == 0


@pytest.mark.asyncio
async def test_search_textbook_by_chapter_filters_correctly():
    """Test that search_textbook_by_chapter applies chapter filter."""
    ctx = MagicMock()
    ctx.context = ChatbotRunContext()

    mock_result = MagicMock()
    mock_result.id = str(uuid4())
    mock_result.score = 0.90
    mock_result.payload = {
        "content": "Humanoid robots are designed to resemble human body structure.",
        "chapter": "chapter-02",
        "chapter_title": "Humanoid Robot Design",
        "section": "section-2-1",
        "section_title": "Introduction to Humanoid Robots",
        "page_path": "/docs/chapter-02/humanoid-design",
        "chunk_index": 0,
        "token_count": 96,
        "created_at": datetime.utcnow().isoformat(),
    }

    with patch('chatbot.tools.qdrant_retriever.qdrant_client') as mock_client:
        mock_client.search = AsyncMock(return_value=[mock_result])

        with patch('chatbot.tools.qdrant_retriever.embedding_service') as mock_embedding:
            mock_embedding.generate_embedding = AsyncMock(return_value=[0.1] * 1536)

            result = await search_textbook_by_chapter(
                ctx,
                chapter="chapter-02",
                query="humanoid robots"
            )

            # Verify chapter filter was applied
            mock_client.search.assert_called_once()
            call_kwargs = mock_client.search.call_args.kwargs
            assert "query_filter" in call_kwargs

            assert "Humanoid robots" in result
            assert len(ctx.context.retrieved_chunks) == 1
