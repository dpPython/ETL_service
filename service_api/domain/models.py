from sqlalchemy import Column, String, Numeric, DateTime, MetaData, Table
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

contract = Table(
                 'contract', metadata,
                 Column('id', UUID, primary_key=True),
                 Column('title', String(50), nullable=False),
                 Column('amount', Numeric),
                 Column('start_date', DateTime),
                 Column('end_date', DateTime),
                 Column('customer', String(50), nullable=False),
                 Column('executor', String(50), nullable=False),
                 )
