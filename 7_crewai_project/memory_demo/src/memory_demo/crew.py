from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class MemoryDemo:
    """Memory Demo Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def support_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['support_agent'],
            # memory=True, # It's optional, by default memory received through crew, make it False, to skip memory for the agent
            verbose=True
        )

    @task
    def support_task(self) -> Task:
        return Task(
            config=self.tasks_config['support_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.support_agent()],
            tasks=[self.support_task()],
            process=Process.sequential,
            memory=True,
            verbose=True,
            chat_llm="openai/gpt-4o",  # Required for chat mode
            tracing=False
        )