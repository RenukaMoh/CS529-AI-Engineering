from typing import List
from crewai.agents.agent_builder.base_agent import BaseAgent
# Import CrewAI core building blocks (Agent/Task/Crew/Process) 
from crewai import Agent, Crew, Process, Task
# CrewAI “project mode” helpers: CrewBase is the base class for a structured crew project, 
# and @agent/@task/@crew decorators register factory methods that build agents, tasks, and the final crew.
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class Debate():  # Debate is the class name, it can be any name you want, it is used to create the crew. The name automatically becomes the name of the project
    """Debate crew"""
# Path to the agents and tasks configuration files stored in the config folder
   # agents_config = 'config/agents.yaml' 
   # tasks_config = 'config/tasks.yaml'
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def debater(self) -> Agent:
        # Build the "debater" agent using the YAML block named 'debater'.
        return Agent(
            config=self.agents_config['debater'],
            verbose=True,
        )

    @agent
    def judge(self) -> Agent:
        # Build the "judge" agent using the YAML block named 'judge'.
        return Agent(
            config=self.agents_config['judge'],
            verbose=True
        )

    @task
    def propose(self) -> Task:
        # Build the "propose" task using the YAML block named 'propose'.
        return Task(
            config=self.tasks_config['propose'],
        )

    @task
    def oppose(self) -> Task:
        # Build the "oppose" task using the YAML block named 'oppose'.
        return Task(
            config=self.tasks_config['oppose'],
        )

    @task
    def decide(self) -> Task:
        # Build the "decide" task using the YAML block named 'decide' for the judge agent.
        return Task(
            config=self.tasks_config['decide'],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Debate crew"""
    # Assemble agents + tasks into one runnable Crew pipeline as a final unit.
        return Crew(
            agents=self.agents, # Auto-collected list of Agent objects from all @agent methods.
            tasks=self.tasks, # Auto-collected list of Task objects from all @task methods.
            process=Process.sequential, # Run the tasks in sequence order propose->oppose->decide.
            verbose=True, # Print end-to-end crew execution trace.
            tracing=True
        )
