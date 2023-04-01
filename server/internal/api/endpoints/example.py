from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from internal.db.database import get_session
from internal.utils.csv.main import put_companies

router = APIRouter()


@router.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome"}


@router.get("/companies", tags=["companies"])
def test(session: AsyncSession = Depends(get_session)):
    put_companies(session)
    return 'ok'
