
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from internal.db.database import get_session
from internal.crud.purchases import get_data_purchases, get_avg_purchases

router = APIRouter()


@router.get("/data_days")
async def get_data_by_days(days: int, session: AsyncSession = Depends(get_session)):
    try:
        return await get_data_purchases(session)
    except Exception as error:
        raise HTTPException(status_code=403)


@router.get("/average_price")
async def average_price_by_days(days_ago: int, session: AsyncSession = Depends(get_session)):
    # try:
    return await get_avg_purchases(days_ago, session)
    # except Exception as error:
    #     raise HTTPException(status_code=403)
