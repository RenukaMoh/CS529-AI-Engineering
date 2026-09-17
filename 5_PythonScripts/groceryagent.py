# Necessary imports
from agents import Agent, Runner, trace
import asyncio
import os
from dotenv import load_dotenv

# Load OpenAI API Key
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

ginstructions="""
You are a smart kitchen assistant.

When given a list of ingredients at home, do the following:
1. Suggest 2 recipes the user can make with these ingredients.
2. For each recipe, provide:
   - A recipe name
   - A short one-line description
   - The required ingredients
3. Identify what ingredients are missing and generate a grouped grocery list.
"""

# Create the Smart Grocery Agent
agent = Agent(
    name="Smart Grocery Agent",
    instructions=ginstructions,
    model="gpt-4o-mini",  
)
print(agent)

# Function to call the agent
async def get_suggestions(user_ingredients: str):
    result = await Runner.run(agent, user_ingredients)
    return result.final_output

    # To retrieve the result from the coroutine object, we need to use the await keyword
 
user_input = "eggs, milk, butter and bread";

async def main():
    response = await (get_suggestions(user_input))
    print(response.final_output)

if __name__ == "__main__":
  asyncio.run(main())

  """ To run the code go to Terminal and the respective folder using cd command and do uv run file.py
  (base) renukamohanraj@Renuka-CSs-MacBook-Air CS589AICourse % cd 5_PythonScripts
  (base) renukamohanraj@Renuka-CSs-MacBook-Air 5_PythonScripts % uv run groceryagent.py
  """