from crewai import Agent, Task, Crew
from crewai.mcp import MCPServerStdio
from crewai.mcp.filters import create_static_tool_filter
from dotenv import load_dotenv

load_dotenv()


# Time MCP Server
time_mcp = MCPServerStdio(
    command="uvx",
    args=[
        "mcp-server-time",
        "--local-timezone=America/Chicago",
    ],
    tool_filter=create_static_tool_filter(
        allowed_tool_names=["get_current_time", "convert_time"]
    ),
    cache_tools_list=True,
)


# Fetch MCP Server
fetch_mcp = MCPServerStdio(
    command="uvx",
    args=["mcp-server-fetch"],
    tool_filter=create_static_tool_filter(
        allowed_tool_names=["fetch"]
    ),
    cache_tools_list=True,
)


# Agent
mcp_agent = Agent(
    role="MCP Information Assistant",
    goal="Answer questions using the appropriate MCP server.",
    backstory=(
        "You can use the Time MCP tools for time and timezone conversions. "
        "You can use the Fetch MCP tool to retrieve webpage content. "
        "Whenever you use Fetch, set raw=true. "
        "If an MCP tool fails, report the failure instead of answering "
        "from your own knowledge."
    ),
    mcps=[time_mcp, fetch_mcp],
    verbose=False,
)


# Task
mcp_task = Task(
    description="Answer the following question using the appropriate MCP tool: {question}",
    expected_output="A clear answer based on the MCP tool result.",
    agent=mcp_agent,
)


# Crew
crew = Crew(
    agents=[mcp_agent],
    tasks=[mcp_task],
    verbose=False,
)


# Run
if __name__ == "__main__":
    questions = [
        (
            "When it is 4:00 PM in Fairfield, Iowa "
            "(America/Chicago), what time is it in India "
            "(Asia/Kolkata)?"
        ),
        (
            "Call the Fetch MCP tool with these exact arguments: "
            "url='https://www.python.org/about/', "
            "raw=true, max_length=5000. "
            "Summarize only the retrieved content in three bullet points."
        ),
    ]

    for question in questions:
        print(f"\n{'~' * 90}")
        print(f"Question: {question}")
        print("~" * 90)

        result = crew.kickoff(inputs={"question": question})
        print(f"Answer: {result}")