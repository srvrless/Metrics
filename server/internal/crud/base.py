from sqlalchemy import func, select
from internal.db.models import Purchases, Companies, Capitalization


async def capitalization_company(session):
    sum_query = select(Purchases.customer_inn.label('company_inn'),
                       func.sum(Purchases.price).label('total_purchase')).\
        where(Purchases.customer_inn.in_(
            select(Companies.supplier_inn).
            where(Purchases.customer_inn == Companies.supplier_inn))).\
        group_by('company_inn')
    result = await session.execute(sum_query)
    # rows = result.fetchmany(100)
    # for row in rows:
    #     print(row)
    # return rows
    async for row in result:
        purchase = Capitalization(
            company_inn=row[0],
            total_purchase=row[1]
        )
        session.add(purchase)

    await session.commit()


async def capitalization_of_each_company(session):
    total_capitalization = await session.scalar(select(func.sum(Capitalization.total_purchase)))

    query = select(
        Capitalization.company_inn,
        (Capitalization.total_purchase / total_capitalization) * 100
    )

    result = await session.all(query)
    return result
