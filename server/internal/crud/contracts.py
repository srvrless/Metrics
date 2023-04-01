
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from internal.db.models import Contracts


async def get_data_contracts(session: AsyncSession):
    stmt = select(
        func.date_trunc(
            'day', Contracts.contract_conclusion_date).label('date'),
        func.count().label('count')
    ).select_from(Contracts).group_by('date')
    rows = await session.execute(stmt)
    result = [row[0] for row in rows.fetchall()]
    return result


async def get_contracts_by_date(session: AsyncSession):
    contract_date = get_data_contracts(session)
    select