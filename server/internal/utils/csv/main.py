from csv import DictReader
from typing import Callable, Any

from sqlalchemy.ext.asyncio import AsyncSession

from internal.db.models import Companies

ARTICLES_COUNT: int = 1000
SPLIT_FUNCTION: Callable[[list], list] = lambda x: x[:ARTICLES_COUNT]


def put_companies(session: AsyncSession):
    with open('./internal/utils/csv/files/companies.csv', newline='\n', encoding='utf-8') as f:
        lines = list(f)
    rows = DictReader(lines, delimiter=';')

    for article in rows:
        session.add(Companies(**article))

