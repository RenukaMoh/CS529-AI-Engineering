# AI-Powered Course Support Crew
# CrewAI Hierarchical Process with LLM Manager

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()

# -------------------------
# Agents
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
# Tasks
# -------------------------
explain_task = Task(
    description=(
        "If the student query is asking for explanation, teaching, or concept understanding, "
        "explain the topic clearly and simply.\n\n"
        "Student query: {student_query}"
    ),
    expected_output="A simple and clear explanation for the student.",
    agent=tutor_agent
)

study_plan_task = Task(
    description=(
        "If the student query is asking for a study schedule, revision plan, or preparation strategy, "
        "create a short and practical study plan.\n\n"
        "Student query: {student_query}"
    ),
    expected_output="A practical study plan for the student.",
    agent=study_planner_agent
)

quiz_task = Task(
    description=(
        "If the student query is asking for practice questions, MCQs, or a quiz, "
        "create a short quiz with answers.\n\n"
        "Student query: {student_query}"
    ),
    expected_output="A short quiz with answers for the student.",
    agent=quiz_creator_agent
)

# -------------------------
# Crew
# -------------------------
student_support_crew = Crew(
    agents=[tutor_agent, study_planner_agent, quiz_creator_agent],
    tasks=[explain_task, study_plan_task, quiz_task],
    process=Process.hierarchical,
    manager_llm="gpt-4o",
    planning=True,
    verbose=True
)

# -------------------------
# Input
# -------------------------
inputs = {
    "student_query": "Create a 5-day study plan for learning Python basics."
}

result = student_support_crew.kickoff(inputs=inputs)

print("\n=== FINAL OUTPUT ===\n")
print(result)

"""
In hierarchical mode, the manager LLM oversees the work, 
but since multiple tasks are already defined inside the crew,
the system may still use more than one task if it thinks they are helpful. 
So hierarchical is not always strict one-query-to-one-task routing.
"""