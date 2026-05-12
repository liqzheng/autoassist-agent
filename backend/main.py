from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from agent import run_agent
import os
from rag import add_document
from memory import save_history, load_history, clear_history

load_dotenv()

app = FastAPI(title="AutoAssist Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

@app.get("/")
def root():
    return {"status": "AutoAssist Agent is running"}

# @app.post("/chat")
# async def chat(request: ChatRequest):
#     history = sessions.get(request.session_id, [])
#     result = run_agent(request.message, history)
#     history.append({"role": "user", "content": request.message})
#     history.append({"role": "assistant", "content": result["answer"]})
#     sessions[request.session_id] = history
#     return {
#         "answer": result["answer"],
#         "steps": result["steps"],
#         "session_id": request.session_id
#     }

@app.delete("/session/{session_id}")

def clear_session(session_id: str):
    sessions.pop(session_id, None)
    return {"status": "Session cleared"}

@app.post("/upload")
async def upload_document(doc_id: str, text: str):
    result = add_document(text, doc_id)
    return {"status": result}

@app.post("/chat")
async def chat(request: ChatRequest):
    history = load_history(request.session_id)  # 从Redis读历史
    result = run_agent(request.message, history) # Agent处理
    history.append({"role": "user", "content": request.message})
    history.append({"role": "assistant", "content": result["answer"]})
    save_history(request.session_id, history)    # 存回Redis
    return {
        "answer": result["answer"],
        "steps": result["steps"],
        "session_id": request.session_id
    }