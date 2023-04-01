from csv import DictReader
from datetime import datetime
from typing import Callable, Any

from sqlalchemy.ext.asyncio import AsyncSession

from internal.db.models import Companies, Participants, Purchases, Contracts

ARTICLES_COUNT: int = 5000
SPLIT_FUNCTION: Callable[[list], list[dict]] = lambda x: x[:ARTICLES_COUNT]


def get_csv_lines(csv_file: str) -> list[str]:
    with open('./internal/utils/csv/files/'+csv_file, newline='\n', encoding='utf-8') as f:
        lines = list(f)
    return SPLIT_FUNCTION(lines)


def put_companies(session: AsyncSession):
    with open('./internal/utils/csv/files/companies.csv', newline='\n', encoding='utf-8') as f:
        lines = list(f)
    rows = DictReader(lines, delimiter=';')

    for article in rows:
        session.add(Companies(**article))


def put_contracts(session: AsyncSession):
    lines = get_csv_lines('contracts.csv')
    rows = DictReader(lines, delimiter=';')

    for article in rows:
        session.add(Contracts(
        contract_reg_number=article['contract_reg_number'],
        price=float(article['price']),
        contract_conclusion_date=datetime.strptime(article['contract_conclusion_date'], '%Y-%m-%d'),
        contract_id=article['id'],
        ))
