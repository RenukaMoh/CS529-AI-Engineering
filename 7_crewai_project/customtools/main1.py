# Step 0: On the Terminal run this command > uv add yfinance

import yfinance as yf

from typing import Type
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool


# Load OPENAI_API_KEY from the .env file
load_dotenv()


# ---------------------------------------------------------
# 1. Define the tool input
# ---------------------------------------------------------

class StockPriceInput(BaseModel):
    """Input schema for the stock-price tool."""
    symbol: str = Field(
        ...,
        description="Stock ticker symbol, such as AAPL, MSFT, or IBM"
    )

# ---------------------------------------------------------
# 2. Create the custom tool
# ---------------------------------------------------------

class StockPriceTool(BaseTool):
    """Get the latest available stock price."""

    name: str = "Get Stock Price"

    description: str = (
        "Get the latest available stock price for a ticker symbol."
    )

    args_schema: Type[BaseModel] = StockPriceInput

    def _run(self, symbol: str) -> str:
        try:
            ticker_symbol = symbol.strip().upper()
            stock = yf.Ticker(ticker_symbol)

            # Retrieve the most recent available trading data one day period
            data = stock.history(period="1d")

            if data.empty:
                return f"No stock price was found for {ticker_symbol}."

            # Retrieve the last available row
            price = data["Close"].iloc[-1]

            return (
                f"The latest available price of "
                f"{ticker_symbol} is ${price:.2f}."
            )

        except Exception as error:
            return f"Unable to retrieve the stock price: {error}"


# Create an instance of the custom tool
stock_price_tool = StockPriceTool()


# ---------------------------------------------------------
# 3. Create the agent
# ---------------------------------------------------------

stock_agent = Agent(
    role="Stock Price Assistant",

    goal=(
        "Find the latest available price for the stock "
        "requested by the user."
    ),

    backstory=(
        "You are a helpful financial information assistant. "
        "You use the stock-price tool to retrieve stock data "
        "and explain the result clearly."
    ),

    tools=[stock_price_tool],

    llm="gpt-5-mini",

    verbose=True
)


# ---------------------------------------------------------
# 4. Get user input
# ---------------------------------------------------------

stock_symbol = input(
    "Enter a stock ticker symbol, such as AAPL or MSFT: "
)


# ---------------------------------------------------------
# 5. Create the task
# ---------------------------------------------------------

stock_task = Task(
    description=(
        f"Find the latest available stock price for "
        f"{stock_symbol}. You must use the Get Stock Price tool."
    ),

    expected_output=(
        "A short response containing the ticker symbol "
        "and its latest available stock price."
    ),

    agent=stock_agent
)


# ---------------------------------------------------------
# 6. Create and run the crew
# ---------------------------------------------------------

stock_crew = Crew(
    agents=[stock_agent],
    tasks=[stock_task],
    process=Process.sequential,
    verbose=True
)


result = stock_crew.kickoff()


# ---------------------------------------------------------
# 7. Display the final result
# ---------------------------------------------------------

print("\nFinal Result")
print("------------")
print(result)