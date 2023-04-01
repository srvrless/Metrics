from sqlalchemy import Boolean, Column, Float, Integer, String, DateTime, func, ForeignKey
from internal.utils.base import Base


class Purchases(Base):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True)
    purchase_name = Column(String, nullable=False, unique=False)
    lot_name = Column(String, nullable=False, unique=False)
    price = Column(Float, nullable=False, unique=False)
    customer_inn = Column(Integer, nullable=False, unique=True)
    customer_name = Column(String, nullable=False, unique=False)
    delivery_region = Column(String, nullable=False, unique=False)
    publish_date = Column(DateTime, default=func.now())
    contract_category = Column(String, nullable=False, unique=False)


class Participants(Base):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True)
    supplier_inn = Column(Integer, ForeignKey('companies.supplier_inn'), nullable=False)
    is_winner = Column(Boolean, default=False)


class Contracts(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    contract_reg_number = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    contract_conclusion_date = Column(DateTime, nullable=False)
    contract_id = Column(String, nullable=False)

class Companies(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    supplier_inn = Column(Integer, nullable=False, unique=True)
    supplier_kpp = Column(String, nullable=False, unique=True)
    okved = Column(String, nullable=False, unique=True)
    status = Column(Boolean, default=True)
    count_managers = Column(Integer, nullable=False)