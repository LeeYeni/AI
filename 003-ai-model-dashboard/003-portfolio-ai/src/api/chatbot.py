from fastapi import APIRouter
from pydantic import BaseModel
from src.service.chatbot_service import start_chat, get_chatbot_response

router = APIRouter(
    prefix="/api/chatbot",
    tags=["Chatbot"]
)

class ChatRequest(BaseModel):
    session_id: str
    prompt: str

@router.get("/start")
def read_chatbot_start():
    chatbot_response = start_chat()
    return chatbot_response

@router.post("")
async def read_chatbot(request: ChatRequest):
    chatbot_response = await get_chatbot_response(request.session_id, request.prompt)
    return chatbot_response