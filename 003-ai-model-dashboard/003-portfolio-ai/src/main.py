from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.service.nickname_service import get_nickname_from_pool
from src.service.chatbot_service import get_chatbot_response, start_chat

from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    prompt: str
    
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://portfolio.yeni-lab.org",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/nickname")
async def read_nickname():
    nickname = await get_nickname_from_pool()
    return {
        "nickname": nickname
    }

@app.get("/api/chatbot/start")
def read_chatbot_start():
    chatbot_response = start_chat()
    return chatbot_response

@app.post("/api/chatbot")
async def read_chatbot(request: ChatRequest):
    chatbot_response = await get_chatbot_response(request.session_id, request.prompt)
    return chatbot_response