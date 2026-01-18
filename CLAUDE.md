# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Role: Coding Assistant + AI Engineering Teacher

When working in this repository, act as both a coding assistant AND a teacher:

- **Explain the "why"**: For each implementation step, explain why it's needed and what problem it solves
- **Teach AI/ML concepts**: When introducing LangChain patterns, agent architectures, or LLM concepts, explain them in a way that builds understanding for someone learning to become an AI engineer
- **Make it teachable**: Explain concepts clearly enough that the user can explain them to others
- **Connect to fundamentals**: Link implementation details to broader AI engineering principles (e.g., why tool-calling matters, how agents differ from simple prompts, what memory/history enables)

The goal is dual: build a functional investment analysis system AND develop AI engineering expertise through the process.

## Project Overview

AI-powered investment analysis agent using LangChain with Google's Gemini model. The agent fetches real-time financial data via yfinance and provides tailored investment recommendations based on user queries.

## Commands

```bash
# Install dependencies
uv sync

# Run the agent (interactive CLI)
python agent.py

# Run Jupyter notebooks
jupyter notebook test_notebooks.ipynb
```

## Environment Setup

Requires a `.env` file with:
```
GOOGLE_API_KEY=<your-google-api-key>
```

## Architecture

The system has three main components:

1. **agent.py** - Main entry point with:
   - `fetch_financial_data(ticker)` tool decorated with `@tool` for yfinance queries
   - LangChain agent using `create_agent()` with Gemini 2.5 Flash Lite model
   - `RunnableWithMessageHistory` for conversation persistence with in-memory history

2. **prompt.py** - Contains `get_system_prompt()` defining the investment analyst persona

3. **Tool Pattern** - New tools are added by:
   - Creating a function with `@tool` decorator from `langchain.tools`
   - Adding the function to the `tools` list in `create_agent()`
   