import os
import asyncio

from dotenv import load_dotenv
from agents import Agent, Runner
from agents.decorators import tool


# ---------------------------------------------------------
# Load the OpenAI API key from the .env file
# ---------------------------------------------------------

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not found.")


# ---------------------------------------------------------
# CONDITIONAL APPROVAL POLICY
#
# Return True  -> Human approval required; tool pauses.
# Return False -> No approval required; tool executes.
# ---------------------------------------------------------

async def needs_approval(_ctx, params, _call_id) -> bool:

    city = params.get("city", "")

    print("Approval function called")
    print("City received:", city)

    # Human approval is required only for Oakland
    return "Oakland" in city


# ---------------------------------------------------------
# WEATHER TOOL
#
# The approval function is connected to the tool through
# needs_approval=needs_approval.
# ---------------------------------------------------------

@tool(needs_approval=needs_approval)
async def get_temperature(city: str) -> str:
    """Return a simulated temperature for a city."""

    return f"The temperature in {city} is 20° Celsius"


# ---------------------------------------------------------
# CREATE AGENT
# ---------------------------------------------------------

agent = Agent(
    name="Weather Agent",
    instructions="""
    Use the get_temperature tool to answer
    temperature questions.
    """,
    tools=[get_temperature],
    model="gpt-5-mini",
)


# ---------------------------------------------------------
# TEST FUNCTION
#
# Runs the agent and checks whether HITL was triggered.
# ---------------------------------------------------------

async def test_weather(city):

    print("\n" + "=" * 45)
    print(f"Weather Request: {city}")
    print("=" * 45)

    result = await Runner.run(
        agent,
        f"What is the temperature in {city}? "
        "Use the get_temperature tool."
    )

    # If interruptions exist, the tool is waiting
    # for human approval.
    if result.interruptions:

        print("HITL Status: HUMAN APPROVAL REQUIRED")
        print("Tool execution is paused.")

    else:

        print("HITL Status: NO HUMAN APPROVAL REQUIRED")
        print("Result:", result.final_output)


# ---------------------------------------------------------
# RUN TWO TEST CASES
# ---------------------------------------------------------

async def main():

    # CASE 1:
    # Chicago -> condition returns False
    # Tool executes automatically.
    await test_weather("Chicago")

    # CASE 2:
    # Oakland -> condition returns True
    # Tool pauses for human approval.
    await test_weather("Oakland, CA")


# ---------------------------------------------------------
# Start the async Python program
# ---------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())