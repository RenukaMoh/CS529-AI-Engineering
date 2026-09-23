from crewai import Agent, Task, Crew
from crewai.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv()

math_agent = Agent(
    role="Math Assistant",
    goal="Use MCP tools to answer the user's question.",
    backstory="You can use the MCP tools for date difference and percentage change.",
    verbose=True,
    mcps=[
        MCPServerStdio(
            command="python",
            args=["mymcpserver.py"],
            cache_tools_list=True
        )
    ]
)

math_task = Task(
    description=(
        "Find the number of days between 2025-01-01 and 2025-03-01. "
        "Also find the percentage change from 80 to 40."
    ),
    expected_output="A clear final answer with both results.",
    agent=math_agent
)

crew = Crew(
    agents=[math_agent],
    tasks=[math_task],
    verbose=True
)

result = crew.kickoff()
print(result)