from sqlalchemy import Boolean, Column, Float, Integer, String, DateTime, func, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import TIMESTAMP

from internal.utils.base import Base


class Purchases(Base):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True)
    purch_id = Column(String)
    purchase_name = Column(String, nullable=False, unique=False)
    lot_name = Column(String, nullable=False, unique=False)
    price = Column(Float, nullable=False, unique=False)
    customer_inn = Column(Integer, nullable=False, unique=True)
    customer_name = Column(String, nullable=False, unique=False)
    delivery_region = Column(String, nullable=False)
    publish_date = Column(TIMESTAMP, default=func.now())
    contract_category = Column(String, nullable=False, unique=False)


class Participants(Base):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True)
    supplier_inn = Column(Integer, nullable=False)
    is_winner = Column(Boolean, default=False)
    part_id = Column(String)


class Contracts(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    contract_reg_number = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    contract_conclusion_date = Column(DateTime, nullable=False)


class Companies(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    supplier_inn = Column(Integer, nullable=False, unique=False)
    supplier_kpp = Column(String, nullable=False, unique=True)
    okved = Column(String, nullable=False, unique=True)
    status = Column(Boolean, default=True)
    count_managers = Column(BigInteger, nullable=False)


class Capitalization(Base):
    __tablename__ = 'capitalizations'
    id = Column(Integer, primary_key=True)
    total_purchase = Column(Integer, nullable=False)
    company_inn = Column(Integer, nullable=False)
