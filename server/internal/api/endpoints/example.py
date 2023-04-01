import aiohttp
import aiomoex
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from internal.db.database import get_session
from internal.crud.base import capitalization_company

router = APIRouter()
inn = "1234567890"


@router.get("/")
async def guess_capitalizasion(session: AsyncSession = Depends(get_session)):
    return await capitalization_company(session)


@router.get("/")
async def god_damn():
    async with aiohttp.ClientSession() as session:

        # Создаем экземпляр клиента для работы с MOEX API
        moex_client = aiomoex.MoexAsyncClient(session)

        # Получаем данные о капитализации компании по ИНН
        securities = await moex_client.get_market_securities(engine="stock", market="shares", boardid="TQBR", q=f"INN={inn}", columns="SECID,SHORTNAME,INN,MARKETPRICE2,ISSUECAPITALIZATION")

        # Обрабатываем ответ от API
        if securities and securities.data:
            # Получаем данные о капитализации компании
            capitalization = securities.data[0][4]
            print(f"Капитализация компании: {capitalization}")
        else:
            print("Данные не найдены")
