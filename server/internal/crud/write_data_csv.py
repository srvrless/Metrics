import csv
import pandas as pd
from asyncpg import create_pool
from internal.db.models import Contracts
from internal.db import settings


async def read_csv(file):
    df = pd.read_csv(file.file, usecols=['price', 'contract_reg_number', 'contract_conclusion_date'], sep=';')
    df.columns = df.columns.str.strip()

    # удаление кавычек из всех значений DataFrame
    df['contract_conclusion_date'] = df['contract_conclusion_date'].astype(str).str.replace('"', '')

    # конвертация даты в формат datetime.date
    df['contract_conclusion_date'] = pd.to_datetime(df['contract_conclusion_date'], format='%Y-%m-%d').dt.date

    return df


async def write_data(df, session):
    df_dict = df.to_dict('records')
    for row in df_dict[:1000]:
        data = Contracts(**row)
        session.add(data)

    await session.commit()
    return data


pool = None

async def get_pool():
    global pool
    if pool is None:
        pool = await create_pool(f"postgresql://gen_user:145632Db@217.25.89.10:5432/default_db")
    return pool

async def insert_data(file):
    # Получить файловый объект для чтения данных CSV
    csv_file = await file.read()

    # Преобразовать байты CSV-файла в строку и считать данные из нее
    reader = csv.DictReader(csv_file.decode('utf-8').splitlines())
    rows = [dict(row) for row in reader]

  
    try:
        pool = await get_pool()

        async with pool.acquire() as conn:
            async with conn.transaction():
                # Записать данные в базу данных
                for row in rows:
                    data = Contracts(**row)
                    await conn.execute(Contracts.__table__.insert().values(**data.dict()))
    except Exception as e:
        print(f"Error inserting data: {e}")