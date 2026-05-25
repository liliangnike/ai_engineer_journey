from openai import OpenAI

# Connect local Ollama server, default port is 11434
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# Initialize chat context
messages = [
        {
            "role" : "system",
            "content" : "You are a senior C++ and Python expert. Your answer should be concise and accurate, also can provide high performance example code."
        }
]

def chat_with_ai(user_input):
    # Append user input 
    messages.append({"role" : "user", "content" : user_input})

    # send request to local Ollama
    response = client.chat.completions.create(
                model="qwen2.5-coder:7b",
                messages=messages
            )

    # Get AI response
    ai_response = response.choices[0].message.content

    # Save AI response to history
    messages.append({"role" : "assistant", "content" : ai_response})

    return ai_response

if __name__ == "__main__":
    print("--- AI expert is ready (Enter 'exit' to quit) ---")
    while True:
        user_q = input("\nUser: ")
        if user_q.lower() == 'exit':
            break
        print(f"AI: {chat_with_ai(user_q)}")
