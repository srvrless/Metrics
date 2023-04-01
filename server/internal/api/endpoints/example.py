from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from internal.db.database import get_session

router = APIRouter()


@router.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome"}


