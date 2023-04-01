from internal.db.models import Contracts
import pandas as pd


async def read_csv(file):
    df = pd.read_csv(file.file, usecols=[
                     'price', 'contract_reg_number', 'contract_conclusion_date'], sep=';')
    df.columns = df.columns.str.strip()
    # удаление кавычек из всех значений DataFrame
    df['contract_conclusion_date'] = df['contract_reg_number'].astype(str).str.replace('"', '')
    return df


async def write_data(df, session):
    for index, row in df.head(1000).iterrows():
        data = Contracts(
            price=row['price'],
            contract_reg_number=row['contract_reg_number'],
            contract_conclusion_date=row['contract_conclusion_date'],
            # добавьте остальные поля из CSV-файла
        )
        session.add(data)

    await session.commit()
    return data