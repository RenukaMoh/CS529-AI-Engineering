import asyncio
import json
from dotenv import load_dotenv

from agents import (
    Agent,
    Runner,
    function_tool,
    ToolGuardrailFunctionOutput,
    ToolInputGuardrailTripwireTriggered,
)

from agents.tool_guardrails import tool_input_guardrail


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

# Loads OPENAI_API_KEY from the .env file
load_dotenv()


# --------------------------------------------------
# TOOL INPUT GUARDRAIL
# --------------------------------------------------

@tool_input_guardrail
def discount_policy_guardrail(data):
    """
    Checks the arguments before the apply_discount tool executes.

    Company Policy:
    AI agents can apply a maximum discount of 20%.
    """

    # Get the arguments that the agent is sending to the tool
    args = json.loads(data.context.tool_arguments or "{}")

    discount = args.get("discount_percent", 0)

    # Block discounts greater than 20%
    if discount > 20:
        return ToolGuardrailFunctionOutput.raise_exception(
            output_info={
                "reason": "AI agents are authorized to apply a maximum 20% discount.",
                "requested_discount": discount,
            }
        )

    # Allow the tool call
    return ToolGuardrailFunctionOutput.allow(
        output_info={
            "reason": "Discount is within the authorized limit."
        }
    )


# --------------------------------------------------
# FUNCTION TOOL
# --------------------------------------------------

@function_tool(
    tool_input_guardrails=[discount_policy_guardrail]
)
def apply_discount(
    customer_id: str,
    product_id: str,
    discount_percent: float,
) -> str:
    """Apply a promotional discount to a customer's product."""

    return (
        f"Discount successfully applied.\n"
        f"Customer: {customer_id}\n"
        f"Product: {product_id}\n"
        f"Discount: {discount_percent}%"
    )


# --------------------------------------------------
# AGENT
# --------------------------------------------------

sales_agent = Agent(
    name="Sales Assistant",
    model="gpt-5-mini",
    instructions=(
        "You are a sales assistant. "
        "When a customer requests a discount, "
        "use the apply_discount tool."
    ),
    tools=[apply_discount],
)


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

async def main():

    try:

        result = await Runner.run(
            sales_agent,
            #"Give customer C101 a 40% discount on product P500."
            "Give customer C101 a 15% discount on product P500."
        )

        print(result.final_output)

    except ToolInputGuardrailTripwireTriggered as e:

        print("\n❌ Tool Input Guardrail Triggered")
        print("The apply_discount tool was NOT executed.")
        print(e)


# --------------------------------------------------
# RUN PROGRAM
# --------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())


"""
Code Explanation: 

TOOL INPUT GUARDRAIL FLOW

User Request
    ↓
Agent prepares Tool Call
    ↓
Tool Input Guardrail checks arguments
    ↓
SDK provides tool arguments through:
data.context.tool_arguments
    ↓
Policy Check
    ↓
Violation → Tripwire Triggered → Tool does NOT execute
Allowed   → Tool executes

Key Point:
A Tool Input Guardrail validates the agent's proposed tool call
before the tool is executed.
"""