from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()

AWS_KNOWLEDGE_MCP = "https://knowledge-mcp.global.api.aws"

# Agent 1: Uses the remote MCP server to collect official AWS information
research_agent = Agent(
    role="AWS Documentation Researcher",
    goal="Find accurate and current AWS guidance from the AWS Knowledge MCP server.",
    backstory=(
        "You are an expert technical researcher. "
        "You use the AWS Knowledge MCP server to retrieve official AWS documentation, "
        "best practices, and related guidance."
    ),
    mcps=[AWS_KNOWLEDGE_MCP],
    verbose=True,
)

# Agent 2: Explains the findings in simple classroom language
teaching_agent = Agent(
    role="Cloud Concepts Instructor",
    goal="Convert AWS research findings into simple, student-friendly notes.",
    backstory=(
        "You are a patient instructor who explains technical concepts clearly "
        "for MSCS students with short, structured teaching notes."
    ),
    verbose=True,
)

task1 = Task(
    description=(
        "Use the AWS Knowledge MCP tools to research this question:\n"
        "'What is Amazon S3, what are its common use cases, and what are 3 best practices for beginners?'\n\n"
        "Instructions:\n"
        "- Use the MCP tools to find official AWS information\n"
        "- Focus on beginner-friendly and accurate guidance\n"
        "- Return concise notes with key facts"
    ),
    expected_output=(
        "A short research note based on official AWS knowledge, including what S3 is, "
        "common use cases, and 3 beginner best practices."
    ),
    agent=research_agent,
)

task2 = Task(
    description=(
        "Take the research note from the previous task and create a clean teaching explanation.\n\n"
        "Format:\n"
        "1. What Amazon S3 is\n"
        "2. 3 common use cases\n"
        "3. 3 beginner best practices\n"
        "4. A final 2-line classroom takeaway\n\n"
        "Keep the language simple and professional."
    ),
    expected_output=(
        "A student-friendly classroom explanation of Amazon S3 with headings and short bullet points."
    ),
    agent=teaching_agent,
)

crew = Crew(
    agents=[research_agent, teaching_agent],
    tasks=[task1, task2],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff()
print("\n========== FINAL OUTPUT ==========\n")
print(result)