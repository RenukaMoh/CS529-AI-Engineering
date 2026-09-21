
# Required installation: uv add docling

import os

from dotenv import load_dotenv
from crewai import LLM, Agent, Crew, Process, Task
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
from crewai_core.paths import db_storage_path


# Load environment variables from .env
load_dotenv()


# Create a knowledge source from web content
content_source = CrewDoclingSource(
    file_paths=[
        "https://lilianweng.github.io/posts/2024-11-28-reward-hacking",
        "https://lilianweng.github.io/posts/2024-07-07-hallucination",
    ]
)


# Display the knowledge database location
knowledge_path = os.path.join(db_storage_path(), "knowledge")
print(f"Knowledge storage location: {knowledge_path}")


# Configure the language model
llm = LLM(
    model="gpt-4o-mini",
    temperature=0
)


# Agent 1: Research analyst
researcher = Agent(
    role="AI Research Analyst",
    goal="Extract key findings and insights from AI research papers",
    backstory=(
        "You are an expert at analyzing academic papers and "
        "identifying important concepts, methodologies, and conclusions."
    ),
    verbose=True,
    llm=llm
)


# Agent 2: Report writer
writer = Agent(
    role="Technical Report Writer",
    goal="Create clear, well-structured reports from research findings",
    backstory=(
        "You transform complex research findings into clear and "
        "useful reports for stakeholders."
    ),
    verbose=True,
    llm=llm
)


# Task 1: Analyze the web content
research_task = Task(
    description=(
        "Analyze the research papers about {topic}. "
        "Identify the key concepts, methodologies, findings, "
        "and limitations."
    ),
    expected_output=(
        "A detailed analysis with bullet points covering the "
        "major concepts, methods, findings, and limitations."
    ),
    agent=researcher
)


# Task 2: Prepare the report
report_task = Task(
    description=(
        "Create an executive-summary report based on the research "
        "analysis. Include practical recommendations."
    ),
    expected_output=(
        "A professional report containing an executive summary, "
        "key findings, and recommendations."
    ),
    agent=writer,
    context=[research_task],
    output_file="output/ai_research_report.md"
)


# Create the crew and provide shared knowledge
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, report_task],
    process=Process.sequential,
    knowledge_sources=[content_source],
    verbose=True
)


# Run the crew
result = crew.kickoff(
    inputs={
        "topic": "reward hacking and hallucination in AI systems"
    }
)

print("\nFinal Result")
print("------------")
print(result.raw)