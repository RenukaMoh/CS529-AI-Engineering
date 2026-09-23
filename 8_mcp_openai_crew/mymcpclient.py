import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Agent Fucntion
async def run_agent(server, message: str):
    print(f"\nUser Message: {message}")
    print("---------------------------------------------------")

    # Create an agent that knows it can use this MCP server
    agent = Agent(
        name="My MCP Agent",
        instructions=(
            "You are a helpful assistant. "
            "Use the MCP tools when they are useful.\n"
            "- Use 'days_between' for date difference.\n"
            "- Use 'percentage_change' to compare two values.\n"         
        ),
        mcp_servers=[server],  # attach the MCP server here, You may pass one or more servers
    )

    # Call the agent with the user message
    result = await Runner.run(
        starting_agent=agent,
        input=message,
    )

    # Print the final reply from the agent
    print("\nAgent Reply:")
    print(result.final_output)
    print("---------------------------------------------------")


# ---------------------------------------------------------
# Main: start MCP server, list tools and Run the agents
# ---------------------------------------------------------
async def main():
    async with MCPServerStdio(
        name="My MCP Server",
        params={
            "command": "mcp",                 # how to run your MCP server
            "args": ["run", "mymcpserver.py"] # server file name
        },
        cache_tools_list=True, # If True, the tools list will be cached and only fetched from the server once. 
        client_session_timeout_seconds=30,    # give API time to respond
    ) as server:

        # 1) List tools from the MCP server
        
        print("=== Tools Available in the MCP Server ===")
        tools = await server.list_tools()
        for t in tools:
            print(f"- {t.name}")
        print("=========================================\n")

        # 2) Run a few demo queries
        await run_agent(server, "Find days between 2025-01-01 and 2025-03-01.")
        await run_agent(server, "What is the percentage change from 80 to 40?")


if __name__ == "__main__":
    asyncio.run(main())
