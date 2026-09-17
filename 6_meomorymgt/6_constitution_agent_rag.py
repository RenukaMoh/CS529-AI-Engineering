import gradio as gr
from agents import Agent, Runner, FileSearchTool, SQLiteSession

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Instantiate the tool
filesearchtool = FileSearchTool(
    vector_store_ids=["vs_6945f63304288191a8eff40407ced41b"]
)

# Create the agent
agent = Agent(
    name="USConstitutionTool",
    instructions=(
        "You are an AI agent that answers questions from the listed vector store, "
        "which has the US Constitution. Answer in one sentence."
    ),
    tools=[filesearchtool]
)

# To store db in the current working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "userconversations.db")

# Create a session (memory persists)
session = SQLiteSession("userquery_session", DB_PATH)

# Function used by Gradio
async def ask_agent(message, history):
    # Use async runner (safe in Gradio's async environment)
    result = await Runner.run(agent, message, session=session)
    return result.final_output

# Gradio UI
gr.ChatInterface(
    fn=ask_agent,
    title="US Constitution Q&A Assistant",
    description="Answers are retrieved from the vector store using FileSearch.",
).launch(share=True,inbrowser=True, inline=False)

