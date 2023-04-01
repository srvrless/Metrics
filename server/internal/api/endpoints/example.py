from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from internal.db.database import get_session
from internal.utils.csv.main import put_companies, put_participants, put_purchases, put_contracts

router = APIRouter()


@router.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome"}


@router.get("/companies", tags=["companies"])
async def test(session: AsyncSession = Depends(get_session)):
    # put_companies(session)
    # await session.commit()

    # put_participants(session)
    # await session.commit()
    put_contracts(session)
    await session.commit()
    # put_purchases(session)
    # await session.commit()
    return 'ok'
