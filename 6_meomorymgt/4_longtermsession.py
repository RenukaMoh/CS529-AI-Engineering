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

print("Agent Chat with Long Term Memory Session")
print("Type 'exit' or 'quit' to stop.\n")

# Create a session
session = SQLiteSession("qa_session",db_path="messages.db")

while True:
    question = input("You: ").strip()

    if question.lower() in ["exit", "quit"]:
        print("Agent: Goodbye!")
        break

    # Run the agent 
    result = Runner.run_sync(agent, question, session=session)
    print("Agent: ", result.final_output)


"""
Code Summary:Now the agents has the long term memory, when restart the session. 
Conversations recalled from the persisted messages.db.

"""