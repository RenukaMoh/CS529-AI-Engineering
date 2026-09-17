from agents import Agent, Runner
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# Create the agent
agent = Agent(
    name="QuestionAnswer",
    instructions="You are an AI agents that answers questions.",
)

print("Agent Chat with Short Memory")
print("Type 'exit' or 'quit' to stop.\n")

# Simple in-memory conversation history
messages = []

while True:
    # 1️⃣ Read user input
    question = input("You: ").strip()

    # 2️⃣ Exit conditions
    if question.lower() in ["exit", "quit"]:
        print("Agent: Goodbye!")
        break

    if question == "":
        print("Agent: Please enter a question.\n")
        continue

    # 3️⃣ Store user message
    messages.append({
        "role": "user",
        "content": question
    })

    # 4️⃣ Run agent synchronously
    result = Runner.run_sync(agent, messages)

    # 5️⃣ Print agent response
    print("Agent:", result.final_output, "\n")

    # 6️⃣ Store agent response
    messages.append({
        "role": "assistant",
        "content": result.final_output
    })

# Final Chat History
print(messages)

"""
Code Summary:
Maintaining and appending messages to a list is the simplest way to 
implement working memory for an agent. 
This approach mirrors how memory works in most chat interfaces and 
directly follows the message structure used by the OpenAI API.
"""
