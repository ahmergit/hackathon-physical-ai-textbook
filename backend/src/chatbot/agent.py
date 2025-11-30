"""
Main textbook chatbot agent using OpenAI Agents SDK.
"""

from agents import Agent, ModelSettings
from ..config import settings
from .prompts import build_system_prompt
from .tools.qdrant_retriever import search_textbook, search_textbook_by_chapter
# Guardrail disabled for now - can be re-enabled once tuned
# from .guardrails.topic_guard import topic_guardrail


def create_textbook_agent(selected_text: str = None, quick_action: str = None) -> Agent:
    """
    Create the textbook chatbot agent with tools and guardrails.

    Args:
        selected_text: Optional text selected by user
        quick_action: Optional quick action modifier

    Returns:
        Configured Agent instance
    """
    # Build system prompt based on context
    system_prompt = build_system_prompt(
        selected_text=selected_text,
        quick_action=quick_action
    )

    # Create agent with tools
    agent = Agent(
        name="Physical AI Textbook Assistant",
        model=settings.chat_model,
        instructions=system_prompt,
        tools=[search_textbook, search_textbook_by_chapter],
        # Guardrail disabled for now - too restrictive
        # input_guardrails=[topic_guardrail],
        model_settings=ModelSettings(parallel_tool_calls=True),
    )

    return agent
