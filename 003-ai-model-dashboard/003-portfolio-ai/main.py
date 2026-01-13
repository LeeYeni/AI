from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.nickname_service import get_nickname
from src.chatbot_service import get_chatbot_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://portfolio.yeni-lab.org"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/nickname")
async def read_nickname():
    nickname = await get_nickname()
    return {
        "nickname": nickname
    }

@app.get("/api/chatbot")
async def read_chatbot(prompt: str):
    chatbot_response = await get_chatbot_response(prompt)
    return {
        "chatbot_response": chatbot_response
    }