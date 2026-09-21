from crewai import Agent, Task, Crew, Process, LLM
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource

import os
from dotenv import load_dotenv
# Load environment variables from .env
load_dotenv()

# Department knowledge using StringKnowledgeSource
department_content = """
The Computer Science department offers a BS in Computer Science that prepares students for 
successful careers in computer technology and information systems, and offers the option 
of gaining a master's degree in only one additional year.

Our unique MS CS degree (emphasizing modern software development: distributed, parallel, 
and web computing) attracts highly qualified students from around the world, 
and includes practical training at top IT companies.

We've started offering a Data Science track as an option in our Computer Professionals 
Master's Program from October 2017.
"""
# Department Knowledge using String content
department_source = StringKnowledgeSource(content=department_content)

# Faculty knowledge using JSONKnowledgeSource, Keep data files inside knowledge folder only

faculty_source = JSONKnowledgeSource(file_paths=["faculty.json"])

# Temparature 0 to get the precise answer without creativity
llm = LLM(model="gpt-4o-mini", temperature=0)
manager_llm = LLM(model="gpt-4o")

# Department Agent
department_agent = Agent(
    role="Department Information Specialist",
    goal="Provide accurate information about the department",
    backstory="Expert in department history, programs, and general information",
    knowledge_sources=[department_source],
    llm=llm,
    #verbose=True
)

# Faculty Agent
faculty_agent = Agent(
    role="Faculty Information Specialist",
    goal="Provide information about faculty members, qualifications, and subjects",
    backstory="Expert in faculty qualifications and teaching areas",
    knowledge_sources=[faculty_source],
    llm=llm,
    #verbose=True
)

# Create a function to build a fresh crew each time
def create_crew():
    # Single task - manager LLM will route it to the right agent in hierarchical process
    task = Task(
        description="Answer the following question: {question}",
        expected_output="A detailed and accurate answer to the question"
    )
    
    return Crew(
        agents=[department_agent, faculty_agent],
        tasks=[task],
        process=Process.hierarchical,
        # manager agent will decide which agent to call based on the question
        manager_llm=manager_llm,
        #verbose=True
    )

# Run first query
crew1 = create_crew()
result1 = crew1.kickoff(inputs={
    "question": "Who is teaching AI Engineering?"
   # "question": "Did the department offers Data Science Track?"
})
print(result1)

# Run second query with a fresh crew instance
"""
crew2 = create_crew()
result2 = crew1.kickoff(inputs={
    "question": "Did the department offers Data Science Track?"
})
print(result2)
"""