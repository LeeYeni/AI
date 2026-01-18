from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import chatbot, nickname, guestbook
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

app.include_router(chatbot.router)
app.include_router(nickname.router)
app.include_router(guestbook.router)

@app.get("/")
def reed_root():
    return {
        "message": "Yeni Portfolio API is running! 🚀"
    }