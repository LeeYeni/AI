from fastapi import APIRouter
from src.service.nickname_service import get_nickname_from_pool

router = APIRouter(
    prefix="/api/nickname",
    tags=["Nickname"]
)

@router.get("")
async def read_nickname():
    nickname = await get_nickname_from_pool()
    return {"nickname": nickname}