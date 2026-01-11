import os
from langchain.agents import create_agent   
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.structured_output import ToolStrategy
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
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

# Create history
history = InMemoryChatMessageHistory()

# Create an agent
agent = create_agent(
    model=model,
    system_prompt=get_system_prompt(),
    tools=[fetch_financial_data]
),

# Make runnable agent with history
agent_with_history = RunnableWithMessageHistory(
      agent,
      lambda session_id: history,
      input_messages_key="input",
      history_messages_key="history",
  )

# Function to make query to agent
while True:
    text = input("> ")
    if text.lower() in {"exit", "quit"}:
        break
    result = agent_with_history.invoke(
        {"input": text},
        config={"configurable": {"session_id": "local"}}
    )
    print(result)
