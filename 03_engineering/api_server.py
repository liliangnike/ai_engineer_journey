# 1. pip install fastapi uvicorn
# 2. Test: uvicorn api_server:app --reload (console log: "INFO:     Application startup complete.")
# 3. Open another terminal
# 4. curl -X POST "http://127.0.0.1:8000/chat?user_prompt=What%20is%20Project-X-99?"

from fastapi import FastAPI
from rag_agent import RAGAgent

app = FastAPI()
agent = RAGAgent()

@app.post("/chat")
async def chat(user_prompt:str):
    response = agent.get_answer(user_prompt)
    return {"reply": response}
