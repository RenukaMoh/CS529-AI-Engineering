# Pre-built MCP Servers Demo: Time and Fetch

import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()


# -------------------------------------------------------
# Display a section divider in the terminal
# -------------------------------------------------------
def divider(title: str):
    print("\n" + "~" * 90)
    print(title)
    print("~" * 90 + "\n")


# -------------------------------------------------------
# Run the agent and display its response
# -------------------------------------------------------
async def run_agent(agent: Agent, message: str):
    divider(f"User Question: {message}")

    result = await Runner.run(
        starting_agent=agent,
        input=message,
    )

    print("Final Answer:")
    print(result.final_output)
    print()


# -------------------------------------------------------
# Main program
# -------------------------------------------------------
async def main():

    # Start the Time and Fetch MCP servers
    async with (
        MCPServerStdio(
            name="Time MCP Server",
            params={
                "command": "uvx",
                "args": [
                    "mcp-server-time",
                    "--local-timezone=America/Chicago",
                ],
            },
            cache_tools_list=True,
            client_session_timeout_seconds=30,
        ) as time_mcp,

        MCPServerStdio(
            name="Fetch MCP Server",
            params={
                "command": "uvx",
                "args": ["mcp-server-fetch"],
            },
            cache_tools_list=True,
            client_session_timeout_seconds=30,
        ) as fetch_mcp,
    ):

        divider("TOOLS LOADED FROM BOTH MCP SERVERS")

        # Retrieve tools from both MCP servers
        time_tools = await time_mcp.list_tools()
        fetch_tools = await fetch_mcp.list_tools()

        print("Time MCP Server Tools:")
        for tool in time_tools:
            print(f"  - {tool.name}")

        print("\nFetch MCP Server Tools:")
        for tool in fetch_tools:
            print(f"  - {tool.name}")

        print()

        # Create an agent with access to both MCP servers
        agent = Agent(
            name="Multi-MCP Agent",
            instructions=(
                "You are a helpful assistant. "
                "Use the Time MCP tools for time and timezone conversions. "
                "Use the Fetch MCP tool when the user provides a webpage URL. "
                "If an MCP tool fails, clearly report the failure. "
                "Do not answer from your own knowledge when a requested tool fails."
            ),
            mcp_servers=[time_mcp, fetch_mcp],
            model="gpt-4o-mini",
        )

        # Demo 1: Time conversion
        await run_agent(
            agent,
            (
                "When it is 4:00 PM in Fairfield, Iowa "
                "(America/Chicago), what time is it in India "
                "(Asia/Kolkata)?"
            ),
        )

        # Demo 2: Retrieve webpage content
        await run_agent(
        agent,
         (
            "Call the Fetch MCP tool with these exact arguments: "
             "url='https://www.python.org/about/', "
             "raw=true, "
             "max_length=5000. "
             "Then summarize only the retrieved content in three bullet points."
        ),
)

# Run the program
if __name__ == "__main__":
    asyncio.run(main())