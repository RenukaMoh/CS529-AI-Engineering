# src/ai_skill_researcher/crew.py

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool


@CrewBase
class AISkillResearchCrew:
    """Crew to research and report AI skills needed for software developers."""

    # Create the web search tool once 
    search_tool = SerperDevTool()

    # -------- Agents --------
    @agent
    def researcher(self) -> Agent:
        """Find AI skills info from the web and compile research notes."""
        return Agent(
            config=self.agents_config["researcher"],
            tools=[self.search_tool],   # Web search enabled
            verbose=True
        )

    @agent
    def analyst(self) -> Agent:
        """Analyze research and categorize skills into a structured framework."""
        return Agent(
            config=self.agents_config["analyst"],
            verbose=True
        )

    @agent
    def report_writer(self) -> Agent:
        """Write the final student-friendly report from the analysis."""
        return Agent(
            config=self.agents_config["report_writer"],
            verbose=True
        )

    # -------- Tasks --------
    @task
    def research_task(self) -> Task:
        """Run web research and produce structured findings + sources."""
        return Task(config=self.tasks_config["research_task"])

    @task
    def analysis_task(self) -> Task:
        """Convert research into categories, must-have list, and insights."""
        return Task(config=self.tasks_config["analysis_task"])

    @task
    def report_task(self) -> Task:
        """Generate the final report (Executive Summary, Table, Top 10, Tools)."""
        return Task(config=self.tasks_config["report_task"])

    # -------- Crew --------
    @crew
    def crew(self) -> Crew:
        """Run tasks in order: research → analysis → report."""
        return Crew(
            agents=self.agents,           # Auto-collected from @agent
            tasks=self.tasks,             # Auto-collected from @task
            process=Process.sequential,   # Run tasks step-by-step
            verbose=True
        )
