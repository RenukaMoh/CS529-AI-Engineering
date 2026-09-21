# CrewAI Hierarchical Example with Custom Manager Agent

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()

# -------------------------
# Worker Agents
# -------------------------
tutor_agent = Agent(
    role="Tutor Agent",
    goal="Explain academic concepts clearly in simple language.",
    backstory="An expert tutor who helps students understand difficult topics.",
    verbose=True
)

study_planner_agent = Agent(
    role="Study Planner Agent",
    goal="Create short and practical study plans for students.",
    backstory="An academic coach who helps students organize their learning.",
    verbose=True
)

quiz_creator_agent = Agent(
    role="Quiz Creator Agent",
    goal="Create short practice quizzes for students.",
    backstory="An assessment expert who prepares simple quizzes for revision.",
    verbose=True
)

# -------------------------
# Custom Manager Agent
# -------------------------
manager = Agent(
    role="Student Support Manager",
    goal="Understand the student query and delegate it to the most suitable specialist agent.",
    backstory=(
        "You are an academic support coordinator. "
        "Your job is to review the student's request, decide which specialist is the best fit, "
        "and ensure the final response is relevant and focused."
    ),
    verbose=True,
    allow_delegation=True
)

# -------------------------
# Tasks
# -------------------------
explain_task = Task(
    description=(
        "ONLY handle this task if the student is asking for concept explanation or topic understanding.\n\n"
        "Student query: {student_query}"
    ),
    expected_output="A clear and simple explanation for the student.",
    agent=tutor_agent
)

study_plan_task = Task(
    description=(
        "ONLY handle this task if the student is asking for a study plan, revision schedule, "
        "or preparation strategy.\n\n"
        "Student query: {student_query}"
    ),
    expected_output="A short and practical study plan.",
    agent=study_planner_agent
)

quiz_task = Task(
    description=(
        "ONLY handle this task if the student is asking for quiz questions, MCQs, "
        "practice questions, or self-test material.\n\n"
        "Student query: {student_query}"
    ),
    expected_output="A short quiz with answers.",
    agent=quiz_creator_agent
)

# -------------------------
# Crew
# -------------------------
student_support_crew = Crew(
    agents=[tutor_agent, study_planner_agent, quiz_creator_agent],
    tasks=[explain_task, study_plan_task, quiz_task],
    process=Process.hierarchical,
    manager_agent=manager,
    planning=True,
    verbose=True
)

# -------------------------
# Input
# -------------------------
inputs = {
    "student_query": "Create a 5 MCQs on Java OOP."
}

result = student_support_crew.kickoff(inputs=inputs)

print("\n=== FINAL OUTPUT ===\n")
print(result)