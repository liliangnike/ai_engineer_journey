import psutil
import json
from openai import OpenAI

# Initialize client
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# Define the tool function
def get_system_memory():
    """Returns system memory usage in GB."""
    memory = psutil.virtual_memory()
    return {
        "used_gb": round(memory.used / (1024**3), 2),
        "total_gb": round(memory.total / (1024**3), 2)
    }

# Define the tool schema
tools = [{
    "type": "function",
    "function": {
        "name": "get_system_memory",
        "description": "Get the current system memory usage",
        "parameters": {"type": "object", "properties": {}}
    }
}]

def run_conversation(user_prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use the provided tools to answer system queries."},
        {"role": "user", "content": user_prompt}
    ]
    
    # First request: Attempt to get a tool call
    response = client.chat.completions.create(
        model="qwen2.5-coder:7b", 
        messages=messages, 
        tools=tools
    )
    
    msg = response.choices[0].message
    
    # Strategy: Handle both formal tool_calls and "hallucinated" JSON text
    if msg.tool_calls:
        # Standard execution path
        tool_call = msg.tool_calls[0]
        func_name = tool_call.function.name
    elif msg.content and "get_system_memory" in msg.content:
        # Defensive path: Manually extract if model failed to format as tool_call
        print("[DEBUG] Model returned JSON text instead of tool_call, parsing manually.")
        func_name = "get_system_memory"
    else:
        return msg.content

    # Execute tool logic
    if func_name == "get_system_memory":
        result = get_system_memory()
        print(f"[DEBUG] Executing tool: {func_name} with result: {result}")
        return f"System memory usage: {result['used_gb']}GB used out of {result['total_gb']}GB."

    return "Error: Could not determine tool to execute."

if __name__ == "__main__":
    # Test the agent
    print(f"AI: {run_conversation('What is the current memory usage?')}")
