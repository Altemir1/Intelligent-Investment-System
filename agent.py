import os
from langchain.agents import create_agent   
from langchain_google_genai import ChatGoogleGenerativeAI
from prompt import get_system_prompt
from dotenv import load_dotenv
from tools.profile import check_profile_exists, load_profile, save_profile

load_dotenv()

# Instantiate the model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

# Create an agent
agent = create_agent(
    model=model,
    system_prompt=get_system_prompt(),
    tools=[check_profile_exists, load_profile, save_profile]
)
# Helper to extract the last AI response text
def get_response_text(result):
    """Extract the final AI message content from agent result."""
    messages = result.get("messages", [])
    # Find the last AIMessage with content
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            return msg.content
    return "(No response)"

# Structure the conversation details
def structure_conversation(conversation_history):
    """Structure the conversation history for the agent."""

# Interactive loop with memory
print("Investment Agent ready. Type 'exit' to quit.\n")

# Conversation history - persists across the loop
conversation_history = []

while True:
    user_input = input("> ")

    if user_input.lower() in {"exit", "quit"}:
        print("Goodbye!")
        
        break

    # Add user message to history
    conversation_history.append({"role": "user", "content": user_input})

    # Send full history to agent
    result = agent.invoke({"messages": conversation_history})

    # Extract AI response
    response = get_response_text(result)

    # Add AI response to history
    conversation_history.append({"role": "assistant", "content": response})

    print(f"\n{response}\n")
