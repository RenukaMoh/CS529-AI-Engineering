import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner

# Load environment variables from .env
load_dotenv()

# Create the agent (STATELESS)
agent = Agent(
    name="QuestionAnswer",
    instructions="You are an AI agent that answers user questions in a friendly tone.",
)

print("Stateless Agent Chat (No Memory)")
print("Type 'exit' to stop.\n")

while True:
    user_text = input("User: ").strip()

    if user_text.lower() == "exit":
        print("Agent: Goodbye!")
        break
   
    # Each run is independent (NO memory)
    result = Runner.run_sync(agent, user_text)
    print(f"{agent.name}: {result.final_output}\n")

"""
Code Summary: This agent does not remember anything 
because we do not store or pass conversation history. 
Every time the agent runs, it starts fresh with no memory of previous conversations.
"""
