import asyncio
from dotenv import load_dotenv

from agents import (
    Agent,
    Runner,
    function_tool,
    ToolGuardrailFunctionOutput,
    ToolOutputGuardrailTripwireTriggered,
)

from agents.tool_guardrails import tool_output_guardrail


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

# Loads OPENAI_API_KEY from the .env file
load_dotenv()

# --------------------------------------------------
# TOOL OUTPUT GUARDRAIL
# --------------------------------------------------

@tool_output_guardrail
def confidential_document_guardrail(data):
    """
    Checks the result returned by the tool.

    Company Policy:
    CONFIDENTIAL documents must not be passed to the agent.
    """

    # Get the output returned by the tool
    tool_result = str(data.output)

    # Check document classification
    if "CONFIDENTIAL" in tool_result.upper():

        return ToolGuardrailFunctionOutput.raise_exception(
            output_info={
                "reason": "Confidential company information detected."
            }
        )

    # Allow safe/public results
    return ToolGuardrailFunctionOutput.allow(
        output_info={
            "reason": "Document is permitted."
        }
    )


# --------------------------------------------------
# FUNCTION TOOL
# --------------------------------------------------

@function_tool(
    tool_output_guardrails=[confidential_document_guardrail]
)
def search_company_documents(query: str) -> str:
    """
    Simulates searching the company's document system.
    """

    # Simulated confidential document
    if "pricing" in query.lower():
        return (
            "Document: 2027 Product Pricing Strategy\n"
            "Classification: CONFIDENTIAL\n"
            "Content: Internal pricing plans for next year."
        )

    # Simulated public document
    return (
        "Document: Product Return Policy\n"
        "Classification: PUBLIC\n"
        "Content: Customers may return eligible products within 30 days."
    )


# --------------------------------------------------
# AGENT
# --------------------------------------------------

employee_agent = Agent(
    name="Employee Assistant",
    model="gpt-5-mini",
    instructions=(
        "You are an employee support assistant. "
        "Use the search_company_documents tool when an employee "
        "asks for company information."
    ),
    tools=[search_company_documents],
)


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

async def main():

    try:

        result = await Runner.run(
            employee_agent,
            #"Find our pricing strategy for next year."
            "Find the company's product return policy."
        )

        print(result.final_output)

    except ToolOutputGuardrailTripwireTriggered as e:

        print("\n❌ Tool Output Guardrail Triggered")
        print("The confidential tool result was blocked.")
        print(e)


# --------------------------------------------------
# RUN PROGRAM
# --------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())

"""
TOOL OUTPUT GUARDRAIL FLOW

User Request
    ↓
Agent calls the Tool
    ↓
Tool executes and returns a result
    ↓
Tool Output Guardrail checks the result
    ↓
SDK provides the tool result through:
data.output
    ↓
Policy Check
    ↓
Violation → Tripwire Triggered → Result is blocked
Allowed   → Result continues to the Agent

Key Point:
A Tool Output Guardrail validates the result returned by a tool
before the result continues through the agent workflow.
"""
