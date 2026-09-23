import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COURSE_FILE = os.path.join(BASE_DIR, "course_info.txt")


class ReadFileArgs(BaseModel):
    path: str = Field(
        description="Absolute path to the course information file to read"
    )


server_params = StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@modelcontextprotocol/server-filesystem@0.6.2",
        BASE_DIR,
    ],
)


if __name__ == "__main__":
    if not os.path.isfile(COURSE_FILE):
        raise FileNotFoundError(f"Course file not found: {COURSE_FILE}")

    with MCPServerAdapter(server_params, "read_file") as mcp_tools:
        read_tool = mcp_tools["read_file"]

        # Supply the path field missing from the adapted tool schema.
        read_tool.args_schema = ReadFileArgs

        course_agent = Agent(
            role="Course Information Assistant",
            goal="Answer questions using the course information file.",
            backstory=(
                "You are an academic assistant. Read the course file "
                "and answer only from its contents."
            ),
            tools=[read_tool],
            verbose=False,
        )

        course_task = Task(
            description=(
                f"Use read_file with path='{COURSE_FILE}'. "
                "Find the Software Engineering course section. "
                "Answer this question: {question} "
                "Include only the topics for Software Engineering. "
                "Do not reproduce the entire file or topics from other courses."
            ),
            expected_output=(
                "Only the Software Engineering topics, presented as a concise list."
            ),
            agent=course_agent,
        )

        crew = Crew(
            agents=[course_agent],
            tasks=[course_task],
            verbose=False,
        )

        result = crew.kickoff(
            inputs={
                "question": "What topics are covered in Software Engineering?"
            }
        )

        print("\nAnswer:\n")
        print(result.raw)

# --- Demo notes ---
# This CrewAI agent uses the filesystem MCP server to read course_info.txt.
# The server is allowed to access only this project's folder (BASE_DIR).
# The agent calls read_file with COURSE_FILE, then answers the question
# using the file contents. ReadFileArgs supplies the path input that the
# MCP adapter did not include in its generated tool schema.
#
# Setup:
# 1. Keep course_info.txt in the same folder as this script.
# 2. Install Node.js so the npx command is available.
# 3. Install project dependencies: uv sync
#    If setting up from scratch: uv add crewai "crewai-tools[mcp]" python-dotenv
# 4. Set OPENAI_API_KEY in your private .env file.
# 5. Run: uv run python crew_filemcp.py