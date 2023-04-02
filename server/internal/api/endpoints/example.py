import aiohttp
import aiomoex
import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from internal.db.database import get_session
from internal.crud.base import capitalization_company

router = APIRouter()
inn = "1234567890"


@router.get("/")
async def guess_capitalizasion(session: AsyncSession = Depends(get_session)):
    return await capitalization_company(session)


@router.get("/never")
async def god_damn():
    request_url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"
    arguments = {
    "securities.columns": (
        "SECID",
        "REGNUMBER",
        "LOTSIZE",
        "SHORTNAME",
        "ISSUECAPITALIZATION",
        )
    }

    async with aiohttp.ClientSession() as session:
        iss = aiomoex.ISSClient(session, request_url, arguments)
        data = await iss.get()
        df = pd.DataFrame(data["securities"])
        # Отфильтруем только нужные столбцы и сконвертируем в нужный тип данных
        df = df[["SECID", "SHORTNAME", "ISSUECAPITALIZATION"]]
        df["ISSUECAPITALIZATION"] = pd.to_numeric(df["ISSUECAPITALIZATION"])
        # Вычислим суммарную капитализацию всех компаний на рынке
        total_capitalization = df["ISSUECAPITALIZATION"].sum()
        # Вычислим долю каждой компании в суммарной капитализации
        df["CAPITALIZATION_PERCENTAGE"] = df["ISSUECAPITALIZATION"] / total_capitalization * 100
        # Выведем результаты
        print(f"Суммарная капитализация: {total_capitalization}")
        print(df.head())