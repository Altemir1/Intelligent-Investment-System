import os
from langchain.agents import create_agent   
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.structured_output import ToolStrategy
import yfinance as yf
from langchain.tools import tool
from pydantic import BaseModel
from prompt import get_system_prompt
from dotenv import load_dotenv

load_dotenv()

# Instantiate the model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

# Define tools for invsetment analyst
@tool
def fetch_financial_data(ticker: str) -> str:
    """
    Fetch Book data for stocks. Use tickers to fetch definite stock

    Args:
        ticker (str): The stock ticker symbol to fetch data for.

    Returns:
        str: The financial data for the specified stock.
    """
    stock = yf.Ticker(ticker)
    return stock.info
# Create an agent
agent = create_agent(
    model=model,
    system_prompt=get_system_prompt(),
    tools=[fetch_financial_data]
)

# Function to make query to agent
def invoke_query(user_input: str):
    response = agent.invoke({"messages":{"role": "user", "content": user_input}})
    return response

print(invoke_query("What investment strategy would you recommend for a 30-year-old with moderate risk tolerance and a 20-year time horizon?"))