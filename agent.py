import os
import json
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from models.schemas import FundamentalAnalysis, ProfileStatus
from dotenv import load_dotenv
from tools.profile_management import check_profile_exists, load_profile, save_profile
from tools.fundamental_analysis import fetch_yahoo_analyst_forecast, fetch_fundamental_data
from conversation_formatter.formatter import print_turn_history, get_response_text
from prompt import get_orchestrator_prompt, get_fundamental_analyst_prompt, get_profile_manager_prompt

load_dotenv()

# -----------------------------
# Fundamental Analyst Sub-Agent
# -----------------------------

# Model instantiaion
fundamental_analyst_model = ChatGoogleGenerativeAI(model="gemini-2.5-pro")

# Agent creation
fundemantetal_analyst_agent = create_agent(
    model=fundamental_analyst_model,
    system_prompt=get_fundamental_analyst_prompt(),
    tools=[fetch_fundamental_data, fetch_yahoo_analyst_forecast],
    response_format = FundamentalAnalysis
)

# Wrap agent as a tool
@tool("fundamental_analyst", description="Analyzes fundamental data of a stock and provides a score from 0-10 with reasoning.")
def fundamental_analyst_sub_agent(query: str) -> str:
    """Tool that uses the Fundamental Analyst sub-agent to analyze stocks."""
    result = fundemantetal_analyst_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return get_response_text(result)

# -----------------------------
# User Profile Manager Sub-Agent
# -----------------------------

# Model instatiation
user_profile_model = ChatGoogleGenerativeAI(model="gemini-2.5-pro")

# Agent creation
user_profile_agent = create_agent(
    model=user_profile_model,
    system_prompt=get_profile_manager_prompt(),
    tools=[check_profile_exists, load_profile, save_profile],
    response_format=ProfileStatus
)

@tool("profile_manager", description="Manages user profiles: checks existence, loads, saves, and updates profiles.")
def user_profile_sub_agent(query: str) -> str:
    """Tool that uses the User Profile Manager sub-agent to handle user profiles."""
    result = user_profile_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return get_response_text(result)

# -----------------------------
# Main Agent
# -----------------------------

# Instantiate the Main Model
main_model = ChatGoogleGenerativeAI(model="gemini-2.5-pro")

# Create an agent
agent = create_agent(
    model=main_model,
    system_prompt=get_orchestrator_prompt(),
    tools=[user_profile_sub_agent, fundamental_analyst_sub_agent]
)


# Interactive loop with memory
print("Investment Agent ready. Type 'exit' to quit.\n")

# Conversation history - persists across the loop
conversation_history = []
turn_number = 0

while True:
    user_input = input("> ")

    if user_input.lower() in {"exit", "quit"}:
        print("Goodbye!")
        break

    turn_number += 1

    # Add user message to history
    conversation_history.append({"role": "user", "content": user_input})

    # Send full history to agent
    result = agent.invoke({"messages": conversation_history})

    # Print execution trace with tool history
    print_turn_history(result, turn_number)

    # Extract AI response
    response = get_response_text(result)

    # Add AI response to history
    conversation_history.append({"role": "assistant", "content": response})

    print(f"💬 FINAL RESPONSE:\n{response}\n")
