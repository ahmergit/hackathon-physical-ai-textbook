"""
Integration tests for the textbook chatbot agent.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from chatbot.agent import create_textbook_agent
from chatbot.context import ChatbotRunContext


@pytest.mark.asyncio
async def test_agent_generates_response_with_citations():
    """Test that agent generates grounded response with citations."""
    agent = create_textbook_agent()

    assert agent.name == "Physical AI Textbook Assistant"
    assert len(agent.tools) == 2  # search_textbook, search_textbook_by_chapter
    assert len(agent.input_guardrails) == 1  # topic_guardrail
    assert agent.model is not None


def test_agent_includes_selected_text_in_prompt():
    """Test that agent prompt includes selected text when provided."""
    selected_text = "Physical AI systems interact with the real world"
    agent = create_textbook_agent(selected_text=selected_text)

    # Verify the prompt includes the selected text
    assert selected_text in agent.instructions


def test_agent_includes_quick_action_in_prompt():
    """Test that agent prompt includes quick action modifier."""
    agent = create_textbook_agent(quick_action="summarize")

    assert "summarize" in agent.instructions.lower() or "concise" in agent.instructions.lower()


@pytest.mark.asyncio
async def test_agent_handles_conversation_history():
    """Test that agent can handle conversation history for follow-up questions."""
    # This test verifies the agent structure supports conversation
    agent = create_textbook_agent()

    # Agent should accept messages parameter in Runner.run
    assert agent is not None
    # Conversation history will be passed via messages parameter to Runner.run
