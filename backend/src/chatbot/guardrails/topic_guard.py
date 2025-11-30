"""
Topic guardrail to restrict responses to textbook content.
Uses OpenAI Agents SDK guardrail system.
"""

from pydantic import BaseModel
from agents import input_guardrail, GuardrailFunctionOutput, Agent, Runner

from ...config import settings


class TopicCheckOutput(BaseModel):
    """Output from the topic checking agent."""
    is_on_topic: bool
    reason: str
    suggested_topics: list[str] = []


# Topic checking agent (uses cheaper/faster model)
topic_guard_agent = Agent(
    name="Topic Guard",
    model="gpt-4o-mini",  # Fast and cheap for classification
    instructions="""You are a topic classifier for a Physical AI and Humanoid Robotics textbook chatbot.

Your job is to determine if a user's question is related to the textbook content.

ON-TOPIC questions are about:
- Physical AI concepts, principles, and applications
- Humanoid robot design, control, and engineering
- Embodied intelligence and robotics
- Sensors, actuators, and robot hardware
- Motion planning and control systems
- Machine learning for robotics
- Topics explicitly covered in a Physical AI/Robotics textbook

OFF-TOPIC questions include:
- General knowledge questions unrelated to robotics
- Current events, weather, entertainment
- Personal advice or opinions
- Coding help unrelated to robotics
- Math/science topics not directly related to Physical AI
- Requests for actions outside of answering textbook questions

If the question is borderline, be generous and mark it as on-topic if it could reasonably
relate to Physical AI or robotics education.

If off-topic, suggest 2-3 related topics from the textbook the user might want to ask about instead.""",
    output_type=TopicCheckOutput,
)


@input_guardrail
async def topic_guardrail(ctx, agent, input: str) -> GuardrailFunctionOutput:
    """
    Input guardrail that checks if the user's question is on-topic.

    This runs in parallel with the main agent to minimize latency.

    Args:
        ctx: Run context
        agent: The main agent
        input: User's input message

    Returns:
        GuardrailFunctionOutput with tripwire status
    """
    # Run the topic checking agent
    result = await Runner.run(
        topic_guard_agent,
        input=input,
        context=ctx.context,
    )

    output: TopicCheckOutput = result.final_output

    # If off-topic, trigger tripwire
    if not output.is_on_topic:
        # Build suggestions string
        suggestions = ""
        if output.suggested_topics:
            suggestions = "Here are some topics I can help with:\n" + "\n".join(
                f"- {topic}" for topic in output.suggested_topics
            )

        off_topic_message = f"""I'm an AI assistant specifically designed to help with the Physical AI and Humanoid Robotics textbook.

Your question appears to be outside the scope of this textbook: {output.reason}

{suggestions}

Would you like to ask about any of these topics instead?"""

        return GuardrailFunctionOutput(
            tripwire_triggered=True,
            output_info={"message": off_topic_message, "reason": output.reason},
        )

    # On-topic, allow to proceed
    return GuardrailFunctionOutput(
        tripwire_triggered=False,
        output_info={"reason": output.reason},
    )
