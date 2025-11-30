"""
Tests for the chat router and SSE streaming endpoint.
"""

import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch, MagicMock

from main import app


@pytest.mark.asyncio
async def test_chat_endpoint_streams_response():
    """Test that chat endpoint returns SSE stream."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Mock the streaming generator
        with patch('routers.chat.generate_chat_stream') as mock_stream:
            async def mock_generator():
                yield 'data: {"type":"delta","content":"Hello"}\n\n'
                yield 'data: {"type":"done","citations":[]}\n\n'

            mock_stream.return_value = mock_generator()

            response = await client.post(
                "/api/chat",
                json={"message": "What is Physical AI?"}
            )

            assert response.status_code == 200
            assert response.headers["content-type"] == "text/event-stream; charset=utf-8"


@pytest.mark.asyncio
async def test_chat_health_endpoint():
    """Test chat health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/chat/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "chatbot"


@pytest.mark.asyncio
async def test_chat_endpoint_accepts_conversation_history():
    """Test that chat endpoint accepts conversation history."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        with patch('routers.chat.generate_chat_stream') as mock_stream:
            async def mock_generator():
                yield 'data: {"type":"done","citations":[]}\n\n'

            mock_stream.return_value = mock_generator()

            response = await client.post(
                "/api/chat",
                json={
                    "message": "Can you explain more?",
                    "conversation_history": [
                        {"role": "user", "content": "What is Physical AI?"},
                        {"role": "assistant", "content": "Physical AI refers to..."}
                    ]
                }
            )

            assert response.status_code == 200


@pytest.mark.asyncio
async def test_chat_endpoint_accepts_selected_text():
    """Test that chat endpoint accepts selected text parameter (US2)."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        with patch('routers.chat.generate_chat_stream') as mock_stream:
            async def mock_generator():
                yield 'data: {"type":"done","citations":[]}\n\n'

            mock_stream.return_value = mock_generator()

            response = await client.post(
                "/api/chat",
                json={
                    "message": "Explain this",
                    "selected_text": "Physical AI systems interact with the real world"
                }
            )

            assert response.status_code == 200
