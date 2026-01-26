import json

def trim_text(text: str, max_words: int = 30) -> str:
    """Trim text to max_words, adding ellipsis if truncated."""
    if not text:
        return ""
    words = str(text).split()
    if len(words) <= max_words:
        return str(text)
    return " ".join(words[:max_words]) + "..."


def print_turn_history(result: dict, turn_number: int) -> None:
    """Print a beautifully formatted history of the agent's turn."""
    messages = result.get("messages", [])

    print(f"\n{'='*60}")
    print(f"  TURN {turn_number} - EXECUTION TRACE")
    print(f"{'='*60}")

    step = 1
    for msg in messages:
        msg_type = type(msg).__name__

        # User message
        if msg_type == "HumanMessage":
            print(f"\n[Step {step}] 👤 USER INPUT")
            print(f"  └─ {trim_text(msg.content)}")
            step += 1

        # AI message (may contain tool calls)
        elif msg_type == "AIMessage":
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                print(f"\n[Step {step}] 🤖 AI TOOL CALLS")
                for call in msg.tool_calls:
                    tool_name = call.get("name", "unknown")
                    tool_args = call.get("args", {})
                    args_str = json.dumps(tool_args, indent=2) if tool_args else "(no args)"
                    print(f"  ├─ Tool: {tool_name}")
                    print(f"  └─ Args: {trim_text(args_str)}")
                step += 1
            elif msg.content:
                print(f"\n[Step {step}] 🤖 AI RESPONSE")
                print(f"  └─ {trim_text(msg.content)}")
                step += 1

        # Tool response
        elif msg_type == "ToolMessage":
            tool_name = getattr(msg, "name", "unknown")
            print(f"\n[Step {step}] 🔧 TOOL RESULT [{tool_name}]")
            print(f"  └─ {trim_text(msg.content)}")
            step += 1

    print(f"\n{'='*60}\n")

# Helper to extract the last AI response text
def get_response_text(result):
    """Extract the final AI message content from agent result."""
    messages = result.get("messages", [])
    # Find the last AIMessage with content
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            return msg.content
    return "(No response)"