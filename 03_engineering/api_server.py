# 1. pip install fastapi uvicorn
# 2. Test: uvicorn api_server:app --reload (console log: "INFO:     Application startup complete.")
# 3. Open another terminal
# 4. curl -X POST "http://127.0.0.1:8000/chat?user_prompt=What%20is%20Project-X-99?"

# **** For Windows Edge 
# 1. Open Windows cmd, execute "ssh -L 8000:127.0.0.1:8000 username@linux_server_ip"
# 2. Enter into this project, execute "uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload"
# 3. Open Microsoft Edge, input "http://127.0.0.1:8000/docs"
# 4. Click 'chat' and then 'try it out'
# ****

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from rag_agent import RAGAgent

app = FastAPI()
agent = RAGAgent()

class ChatRequest(BaseModel):
    user_prompt:str = Field(..., min_length = 1, max_length = 1000)

@app.post("/chat")
async def chat(request:ChatRequest):
    try:
        response = agent.get_answer(request.user_prompt)
        return {"reply": response}
    except Exception as err:
        logging.error(f"Errors during request processing: {err}")
        raise HTTPException(status_code = 500, detail = "Internal Server Error")
