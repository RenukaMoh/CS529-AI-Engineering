# Demo without Decorator Tools, hardcoding agents and Tasks without yaml file

from typing import Type
from crewai import Agent, Crew, Task, Process
from crewai.tools import BaseTool, tool
from pydantic import BaseModel, Field
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ============ Custom Tool 1: @tool Decorator ============
# name is for the agent/LLM's better understanding
@tool("Get Weather")
def get_weather(city: str) -> str:
    """Fetch current weather for a given city."""
    endpoint = "https://wttr.in"
    #response = requests.get(f"{endpoint}/{city}") # Return full lengthy report
    response = requests.get(f"{endpoint}/{city}?format=3") # Return short one line summary with the style #3
    return response.text

# ============ Custom Tool 2: BaseTool Subclass ============
# Ticker:Apple Inc: AAPL, Tesla: TSLA
class StockPriceInput(BaseModel): # Input Schema
    symbol: str = Field(..., description="Stock ticker symbol")

class StockPriceTool(BaseTool): # Custom Tool
    name: str = "Get Stock Price"
    description: str = "Get current stock price for a ticker symbol."
    args_schema: Type[BaseModel] = StockPriceInput #Assign the schema

    def _run(self, symbol: str) -> str: # Automatic Tool execution
        return f"Current price of {symbol.upper()}: $150.25"

# ============ AGENTS ============
weather_agent = Agent(
    role="Weather Analyst",
    goal="Provide weather information",
    backstory="Expert meteorologist.",
    tools=[get_weather],
    verbose=True
)

stock_agent = Agent(
    role="Stock Analyst",
    goal="Provide stock insights",
    backstory="Financial analyst.",
    tools=[StockPriceTool()],
    verbose=True
)

# ============ TASKS ============
weather_task = Task(
    description="Get weather for New York.",
    expected_output="NYC weather conditions.",
    agent=weather_agent
)

stock_task = Task(
    description="Get Apple (AAPL) stock price.",
    expected_output="AAPL stock price.",
    agent=stock_agent
)

# ============ CREW ============
# By default Sequential process
crew = Crew(
    agents=[weather_agent, stock_agent],
    tasks=[weather_task, stock_task],
    verbose=True
)

# ============ RUN ============
if __name__ == "__main__":
    result = crew.kickoff()
    print(result)