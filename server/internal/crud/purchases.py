
from datetime import datetime, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from internal.db.models import Purchases


async def get_data_purchases(session: AsyncSession):
    stmt = select(
        func.date_trunc(
            'day', Purchases.publish_date).label('date'),
        func.count().label('count')
    ).select_from(Purchases).group_by('date')
    rows = await session.execute(stmt)
    result = [row[0] for row in rows.fetchall()]
    return result


async def get_avg_purchases(days_ago: int, session: AsyncSession):
    # convert the days_ago argument to a datetime object
    dt_days_ago = datetime.now() - timedelta(days=days_ago)

    stmt = select(
        func.date_trunc('day', Purchases.publish_date).label('date'),
        func.avg(Purchases.price).label('average_price')
    ).where(Purchases.publish_date >= dt_days_ago).group_by(Purchases.publish_date, 'date').order_by(Purchases.publish_date)

    result = await session.execute(stmt)  # await the async function
    rows = result.fetchall()

    data = {row[0].strftime("%Y-%m-%d"): row[1] for row in rows}

    return data