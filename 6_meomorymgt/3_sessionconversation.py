from agents import Agent, Runner, SQLiteSession
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# Create the agent
agent = Agent(
    name="QuestionAnswer",
    instructions="You are an AI agents that answers questions.",
)

print("Agent Chat with Session Memory")
print("Type 'exit' or 'quit' to stop.\n")

# Create a session
session = SQLiteSession("first_session")

while True:
    question = input("You: ").strip()

    if question.lower() in ["exit", "quit"]:
        print("Agent: Goodbye!")
        break

    # Run the agent 
    result = Runner.run_sync(agent, question, session=session)
    print("Agent: ", result.final_output)


"""
Code Summary:
Sessions provide an easy way to add working memory to an agent. 
By assigning a unique session_id, each conversation maintains its own 
isolated memory context. 

Memory is lost when the program stops.
"""