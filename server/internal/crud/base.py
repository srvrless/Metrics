import spacy
from sqlalchemy import func, select
from internal.db.models import Purchases, Companies, Capitalization

# Загружаем модель языка
nlp = spacy.load("en_core_web_sm")

categories = {
    "Электроника": ["телефон", "ноутбук", "планшет", "телевизор"],
    "Одежда": ["брюки", "рубашка", "платье", "куртка"],
    "Косметика": ["шампунь", "гель для душа", "крем для лица", "тушь для ресниц"],
    "Еда": ["сыр", "мясо", "овощи", "фрукты"]
}

async def capitalization_company(session):
    sum_query = select(Purchases.customer_inn.label('company_inn'),
                       func.sum(Purchases.price).label('total_purchase')).\
        where(Purchases.customer_inn.in_(
            select(Companies.supplier_inn).
            where(Purchases.customer_inn == Companies.supplier_inn))).\
        group_by('company_inn')
    result = await session.execute(sum_query)
    rows = result.fetchmany(100)
    for row in rows:
        print(row)
    # return rows
    # async for row in result:
    #     purchase = Capitalization(
    #         company_inn=row[0],
    #         total_purchase=row[1]
    #     )
    #     session.add(purchase)

    # await session.commit()


async def capitalization_of_each_company(session):
    # Берем всю капитализацию
    total_capitalization = await session.scalar(select(func.sum(Capitalization.total_purchase)))
    # Подсчитываем капитализацию каждой компании
    query = select(
        Capitalization.company_inn,
        (Capitalization.total_purchase / total_capitalization) * 100
    )

    result = await session.all(query)
    return result


async def categorize_product(product_name):
    # Преобразуем название товара в объект Doc
    doc = nlp(product_name.lower())
    
    # Проходимся по всем словам в названии товара
    for token in doc:
        # Проверяем, присутствует ли текущее слово в словаре категорий товаров
        for category, keywords in categories.items():
            if token.text in keywords:
                return category
                
    # Если ни одно ключевое слово не было найдено, возвращаем значение "Неизвестно"
    return "Undefined"

