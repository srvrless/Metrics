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
    lines = get_csv_lines('companies.csv')
    rows = DictReader(lines, delimiter=';')

    for article in rows:
        if not article['name']:
            continue
        session.add(Companies(name=article['name'],
                              supplier_inn=article['supplier_inn'],
                              supplier_kpp=article['supplier_kpp'],
                              okved=article['okved'],
                              status=False if article['status'] == 'Заблокирована' else True,
                              count_managers=int(article['count_managers'])
                              ))


def put_participants(session: AsyncSession):
    lines = get_csv_lines('participants.csv')
    rows = DictReader(lines, delimiter=';')

    for article in rows:
        session.add(Participants(
            part_id=int(article['id'].split('_')[-1]),
            supplier_inn=article['supplier_inn'],
            is_winner = article['is_winner'] == 'Да'
        ))


def put_purchases(session: AsyncSession):
    lines = get_csv_lines('purchases.csv')
    rows = DictReader(lines, delimiter=';')

    for article in rows:
        session.add(Purchases(
        purchase_name = article['purchase_name'],
        lot_name = article['lot_name'],
        price = float(article['price']),
        customer_inn = article['customer_inn'],
        customer_name = article['customer_name'],
        delivery_region = article['delivery_region'],
        publish_date = datetime.strptime(article['publish_date'], '%Y-%m-%d %H:%M:%S.%f'),
        contract_category = article['contract_category'],
        ))


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

