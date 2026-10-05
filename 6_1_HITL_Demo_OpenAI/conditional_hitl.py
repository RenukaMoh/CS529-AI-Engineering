import os
import asyncio

from dotenv import load_dotenv
from agents import Agent, Runner
from agents.decorators import tool


# ---------------------------------------------------------
# 1. LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not found.")


# ---------------------------------------------------------
# 2. CONDITIONAL APPROVAL POLICY
#
# Purpose: Decide whether the weather tool needs human approval.
# Input:   Tool arguments through params.
# Process: Check the requested city.
# Output:  True  -> HITL approval required
#          False -> Tool executes automatically
# ---------------------------------------------------------

async def requires_oakland_approval(_ctx, params, _call_id) -> bool:

    city = params.get("city", "")

    print("Approval function called")
    print("City received:", city)

    # Human approval is required only for Oakland.
    return "Oakland" in city


# ---------------------------------------------------------
# 3. WEATHER TOOL
#
# The approval policy is connected to the tool using
# needs_approval=requires_oakland_approval.
# ---------------------------------------------------------

@tool(needs_approval=requires_oakland_approval)
async def get_temperature(city: str) -> str:
    """Return a simulated temperature for a city."""

    return f"The temperature in {city} is 20° Celsius."


# ---------------------------------------------------------
# 4. CREATE AGENT
# ---------------------------------------------------------

agent = Agent(
    name="Weather Agent",
    instructions="""
    Use the get_temperature tool to answer temperature questions.
    """,
    tools=[get_temperature],
    model="gpt-6-astra",
)


# ---------------------------------------------------------
# 5. TEST WEATHER REQUEST
#
# Purpose: Run a weather request and demonstrate conditional HITL.
# Input:   City name.
# Process: Run the agent and check for an HITL interruption.
# Output:  Automatic result or human approval/rejection result.
# ---------------------------------------------------------

async def test_weather(city):

    print("\n" + "=" * 45)
    print(f"Weather Request: {city}")
    print("=" * 45)

    # Start the agent workflow.
    result = await Runner.run(
        agent,
        f"What is the temperature in {city}? "
        "Use the get_temperature tool."
    )

    # -----------------------------------------------------
    # CASE: HUMAN APPROVAL REQUIRED
    # -----------------------------------------------------

    if result.interruptions:

        print("HITL Status: HUMAN APPROVAL REQUIRED")
        print("Tool execution is paused.")

        # Convert the paused result into RunState.
        # This state is needed to resume the same workflow.
        state = result.to_state()

        # Get the tool call that is waiting for human approval.
        interruption = result.interruptions[0]

        print("Tool:", interruption.name)
        print("Arguments:", interruption.arguments)

        # Ask the human reviewer for a decision.
        decision = input("\nApprove weather tool? (yes/no): ")

        if decision.strip().lower() == "yes":

            # Record the human approval in RunState.
            state.approve(interruption)

            print("Human Decision: APPROVED")

        else:

            reason = input("Enter rejection reason: ")

            # Record the rejection and reason in RunState.
            state.reject(
                interruption,
                rejection_message=reason
            )

            print("Human Decision: REJECTED")
            print("Rejection Reason:", reason)

        # Resume the SAME paused workflow after the
        # human approval/rejection decision.
        result = await Runner.run(agent, state)

        print("\nFinal Result:")
        print(result.final_output)

    # -----------------------------------------------------
    # CASE: HUMAN APPROVAL NOT REQUIRED
    # -----------------------------------------------------

    else:

        print("HITL Status: NO HUMAN APPROVAL REQUIRED")
        print("Result:", result.final_output)


# ---------------------------------------------------------
# 6. RUN TWO TEST CASES
# ---------------------------------------------------------

async def main():

    # CASE 1:
    # Chicago -> approval condition returns False.
    # The weather tool executes automatically.
    await test_weather("Chicago")

    # CASE 2:
    # Oakland -> approval condition returns True.
    # The workflow pauses for a human decision.
    await test_weather("Oakland, CA")


# ---------------------------------------------------------
# 7. START THE ASYNC PYTHON PROGRAM
# ---------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())