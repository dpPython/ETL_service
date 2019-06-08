from sqlalchemy import Column, String, Numeric, Date, MetaData, Table
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

contract = Table(
                 'contract', metadata,
                 Column('id', UUID, primary_key=True),
                 Column('title', String(50), nullable=False),
                 Column('amount', Numeric),
                 Column('start_date', Date),
                 Column('end_date', Date),
                 Column('customer', String(50), nullable=False),
                 Column('executor', String(50), nullable=False),
                 )
