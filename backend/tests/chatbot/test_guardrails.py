"""
Tests for chatbot guardrails.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from chatbot.guardrails.topic_guard import topic_guardrail, TopicCheckOutput
from chatbot.context import ChatbotRunContext


@pytest.mark.asyncio
async def test_topic_guardrail_allows_on_topic_questions():
    """Test that topic guardrail allows on-topic questions."""
    # Mock context and agent
    ctx = MagicMock()
    ctx.context = ChatbotRunContext()
    agent = MagicMock()

    # Mock the topic guard agent to return on-topic
    mock_result = MagicMock()
    mock_result.final_output = TopicCheckOutput(
        is_on_topic=True,
        reason="Question is about Physical AI concepts",
        suggested_topics=[]
    )

    with patch('chatbot.guardrails.topic_guard.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        result = await topic_guardrail(ctx, agent, "What is Physical AI?")

        assert result.tripwire_triggered is False
        assert "reason" in result.output_info


@pytest.mark.asyncio
async def test_topic_guardrail_blocks_off_topic_questions():
    """Test that topic guardrail blocks off-topic questions."""
    ctx = MagicMock()
    ctx.context = ChatbotRunContext()
    agent = MagicMock()

    # Mock the topic guard agent to return off-topic
    mock_result = MagicMock()
    mock_result.final_output = TopicCheckOutput(
        is_on_topic=False,
        reason="Question is about weather, not related to Physical AI",
        suggested_topics=["Physical AI concepts", "Humanoid robot design", "Sensor systems"]
    )

    with patch('chatbot.guardrails.topic_guard.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        result = await topic_guardrail(ctx, agent, "What's the weather today?")

        assert result.tripwire_triggered is True
        assert "message" in result.output_info
        assert "Physical AI" in result.output_info["message"]


@pytest.mark.asyncio
async def test_topic_guardrail_provides_suggestions():
    """Test that topic guardrail provides topic suggestions when off-topic."""
    ctx = MagicMock()
    ctx.context = ChatbotRunContext()
    agent = MagicMock()

    mock_result = MagicMock()
    mock_result.final_output = TopicCheckOutput(
        is_on_topic=False,
        reason="Question is unrelated to robotics",
        suggested_topics=["Robot control systems", "Actuator design"]
    )

    with patch('chatbot.guardrails.topic_guard.Runner') as mock_runner:
        mock_runner.run = AsyncMock(return_value=mock_result)

        result = await topic_guardrail(ctx, agent, "How do I bake a cake?")

        assert result.tripwire_triggered is True
        assert "Robot control systems" in result.output_info["message"]
        assert "Actuator design" in result.output_info["message"]
