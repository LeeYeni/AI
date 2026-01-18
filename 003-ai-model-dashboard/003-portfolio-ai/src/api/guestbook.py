from fastapi import APIRouter
from pydantic import BaseModel
from src.service.guestbook_service import save_guestbook_message, get_guestbook_messages

router = APIRouter(
    prefix="/api/guestbook",
    tags=["Guestbook"]
)

class GuestBookRequest(BaseModel):
    nickname: str
    context: str

@router.post("")
async def save_guestbook(request: GuestBookRequest):
    await save_guestbook_message(request.nickname, request.context)

@router.get("")
async def read_guestbook():
    return await get_guestbook_messages()