import io
import pandas as pd
import matplotlib.pyplot as plt
from fastapi import FastAPI, Depends, APIRouter, File, UploadFile
from sqlalchemy import create_engine, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from internal.db.database import get_session
from internal.db.models import Purchases, Contracts
from fastapi.responses import StreamingResponse

from internal.crud.write_data_csv import read_csv, write_data, insert_data

import json
router = APIRouter()


@router.post("/insert-csv-data")
async def insert_csv_data(file: UploadFile = File(...)):
    await insert_data(file)
    return {"message": "Data inserted successfully"}


@router.post('/upload-csv')
async def upload_csv(file: UploadFile = File(...), session: AsyncSession = Depends(get_session)):
    df = await read_csv(file)
    await write_data(df, session)
    return {'status': 'ok'}


@router.get("/purchases")
async def get_purchases_graph(session: AsyncSession = Depends(get_session)):
    # запрос для получения данных о покупках
    stmt = select(
        func.date_trunc('day', Purchases.publish_date).label('date'),
        func.count().label('count')
    ).select_from(Purchases).group_by('date')
    result = await session.execute(stmt)
    rows = result.fetchall()

    df = pd.DataFrame(rows, columns=["date", "count"])
    df.set_index("date", inplace=True)
    return df.plot(kind="bar").get_figure()


@router.get("/contracts")
async def get_contracts_graph(session: AsyncSession = Depends(get_session)):
    stmt = select(
        func.date_trunc(
            'day', Contracts.contract_conclusion_date).label('date'),
        func.count().label('count')
    ).select_from(Contracts).group_by('date')
    rows = await session.execute(stmt)
    result = rows.fetchall()

    # преобразование результата запроса в объект DataFrame
    df = pd.DataFrame(result, columns=['date', 'count'])

    # построение графика с помощью библиотеки Matplotlib
    plt.plot(df['date'], df['count'])
    plt.title('purchases_crud')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.show()

    # преобразование графика в формат PNG и его отправка в ответе API
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return StreamingResponse(buf, media_type='image/png')


@router.get("/get_prices_contracts")
async def get_prices_contacts(session: AsyncSession = Depends(get_session)):
    stmt = select(Purchases.price, Purchases.publish_date,
                  Purchases.delivery_region)
    result = await session.execute(stmt)

    prices = [(row[0], str(row[1]), row[2]) for row in result]
    prices = sorted(prices, key=lambda x: x[1])

    result = {}

    for price in prices:
        key = price[1].split(' ')[0]

        if key not in result:
            result[key] = 0
        result[key] += int(price[0])
        print(price[2])

    f = open("tests_prices.json", "w", encoding="utf-8")
    json.dump(result, f, indent=3)
    f.close()
    return result
