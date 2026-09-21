from crewai import Agent, Crew, Memory, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class CrewaiMemory:
    """Customer-support crew with unified memory."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def support_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["support_agent"],
        )

    @task
    def support_task(self) -> Task:
        return Task(
            config=self.tasks_config["support_task"],
        )

    @crew
    def crew(self) -> Crew:
        shared_memory = Memory(
            storage="./.crewai/memory",
            semantic_weight=0.5,
            recency_weight=0.3,
            importance_weight=0.2,
            recency_half_life_days=30,
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            memory=shared_memory,
            chat_llm="gpt-4o",
            verbose=True,
            tracing=False,
        )