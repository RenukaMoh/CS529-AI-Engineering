import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp
from agents.model_settings import ModelSettings
from dotenv import load_dotenv


load_dotenv()

async def main():
    # Connect to the public DeepWiki remote MCP server
    async with MCPServerStreamableHttp(
        name="DeepWiki MCP Server",
        params={
            "url": "https://mcp.deepwiki.com/mcp",
            "timeout": 30,
        },
        cache_tools_list=True,
        client_session_timeout_seconds=30,
        max_retry_attempts=2,
    ) as server:

        # Display tools provided by the remote MCP server
        tools = await server.list_tools()

        print("\nAvailable Remote MCP Tools:")
        print("-" * 60)

        for tool in tools:
            print(f"Tool: {tool.name}")
            print(f"Description: {tool.description or 'No description provided'}")
            print("-" * 60)

        # Create an agent with access to DeepWiki
        agent = Agent(
            name="Repository Documentation Assistant",
            instructions=(
                "You answer questions about public GitHub repositories. "
                "Always use the DeepWiki MCP tools to inspect the repository. "
                "Base your answer only on information returned by the MCP server. "
                "Do not answer from your own knowledge. "
                "If the requested information is unavailable, clearly say so. "
                "Keep the final answer short and easy to understand."
            ),
            mcp_servers=[server],
            model="gpt-4.1-mini",
            model_settings=ModelSettings(
                tool_choice="required",
            ),
        )

        user_prompt = (
            "Use the DeepWiki MCP tools to examine the GitHub repository "
            "'openai/openai-agents-python'. "
            "Explain three main capabilities of the OpenAI Agents SDK. "
            "Present the answer as three short bullet points."
        )

        result = await Runner.run(
            starting_agent=agent,
            input=user_prompt,
        )

        print("\nFinal Response:")
        print("-" * 60)
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())