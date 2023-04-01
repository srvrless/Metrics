import io
import pandas as pd
import matplotlib.pyplot as plt
from fastapi import FastAPI, Depends, APIRouter, File, UploadFile
from sqlalchemy import create_engine, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from internal.db.database import get_session
from internal.db.models import Purchases, Contracts
from fastapi.responses import StreamingResponse

from internal.crud.write_data_csv import read_csv, write_data

router = APIRouter()


@router.post('/upload-csv')
async def upload_csv(file: UploadFile = File(...), session: AsyncSession = Depends(get_session)):
    df = await read_csv(file)
    await write_data(df,session)
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

#     df = pd.DataFrame(rows, columns=["date", "count"])
#     df.set_index("date", inplace=True)

#     fig, ax = plt.subplots()
#     ax.bar(df.index, df["count"])
#     ax.set_xlabel("Date")
#     ax.set_ylabel("Count")
#     ax.set_title("Contracts")

#     return fig
    # # преобразование результата запроса в объект DataFrame
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
