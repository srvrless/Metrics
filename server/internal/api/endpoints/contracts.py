
from datetime import datetime, timedelta
from sqlalchemy import func,select
from internal.db.models import Purchases
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from internal.db.database import get_session

router = APIRouter()

@router.get("/average_price")
async def get_average_price(days: int ,session: AsyncSession = Depends(get_session)):
    days_ago = datetime.now() - timedelta(days)
    rows=select(Purchases).where(Purchases.publish_date >= days_ago).with_only_columns(func.avg(Purchases.price))
    result = await session.execute(rows)
    return {"average_price": result.scalars().all()}
