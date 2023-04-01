from csv import DictReader
from typing import Callable, Any

from sqlalchemy.ext.asyncio import AsyncSession

from internal.db.models import Companies, Participants

ARTICLES_COUNT: int = 1000
SPLIT_FUNCTION: Callable[[list], list[dict]] = lambda x: x[:ARTICLES_COUNT]


def get_csv_lines(csv_file: str) -> list[str]:
    with open('./internal/utils/csv/files/'+csv_file, newline='\n', encoding='utf-8') as f:
        lines = list(f)
    return SPLIT_FUNCTION(lines)


def put_companies(session: AsyncSession):
    lines = get_csv_lines('companies.csv')
    rows = DictReader(lines, delimiter=';')

    for article in rows:
        if not article['name']:
            continue
        session.add(Companies(name=article['name'],
                              supplier_inn=int(article['supplier_inn']),
                              supplier_kpp=article['supplier_kpp'],
                              okved=article['okved'],
                              status=False if article['status'] == 'Заблокирована' else True,
                              count_managers=int(article['count_managers'])
                              ))


def put_participants(session: AsyncSession):
    lines = get_csv_lines('participants.csv')
    rows = DictReader(lines, delimiter=';')

    for article in rows:
        session.add(Participants(**article))

