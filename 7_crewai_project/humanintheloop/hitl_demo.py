from crewai import Agent, Task, Crew

import os
from dotenv import load_dotenv
# Load environment variables from .env
load_dotenv()

# ---- AGENT 1: Researcher ----
researcher = Agent(
   role="Senior Research Analyst",
   goal="Find the latest AI trends and breakthroughs in 2025",
   backstory=(
       "You work at a top tech think tank. You're an expert at "
       "finding emerging trends and presenting actionable insights."
   ),
   verbose=True,
)
# ---- AGENT 2: Editor ----
editor = Agent(
   role="Content Editor",
   goal="Review research for accuracy, clarity, and completeness",
   backstory=(
       "You are a meticulous editor with 10 years of experience "
       "in tech publishing. You ensure every fact is verified."
   ),
   verbose=True,
)
# ---- AGENT 3: Writer ----
writer = Agent(
   role="Blog Writer",
   goal="Turn edited research into an engaging blog post",
   backstory=(
       "You are a creative tech writer known for making complex "
       "topics simple and fun to read."
   ),
   verbose=True,
)

# ---- TASK 1: Research (Human reviews the research) ----
research_task = Task(
   description=(
       "Research the top 5 AI advancements in 2025. "
       "Include key players, technologies, and real-world impact."
   ),
   expected_output="A detailed bullet-point report of top 5 AI advancements",
   agent=researcher,
   human_input=True,  # YOU review the research before it moves on
)
# ---- TASK 2: Edit (No human review, agent handles it) ----
edit_task = Task(
   description=(
       "Review the researcher's report. Fix any inaccuracies, "
       "remove fluff, and ensure the facts are solid."
   ),
   expected_output="A clean, fact-checked version of the research report",
   agent=editor,
)

# ---- TASK 3: Write Blog (Human reviews final blog) ----
write_task = Task(
   description=(
       "Using the edited research, write a 3-paragraph blog post. "
       "Make it engaging, informative, and accessible."
   ),
   expected_output="A polished 3-paragraph markdown blog post",
   agent=writer,
   human_input=True,  # YOU review the final blog before publishing
   output_file="blog_post.md",  # saves the final output to a file
)
crew = Crew(
   agents=[researcher, editor, writer],
   tasks=[research_task, edit_task, write_task],
   verbose=True,
)

result = crew.kickoff()
print(result)
