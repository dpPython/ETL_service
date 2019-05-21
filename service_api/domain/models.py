from sqlalchemy import *

metadata = MetaData()

payment = Table(
    "payment",
    metadata,
    Column("id", String, primary_key=True, nullable=False),
    Column("contributor", VARCHAR(50), nullable=False),
    Column("amount", Float, nullable=False),
    Column("date", DateTime, nullable=False),
    Column("contract_id", String, nullable=False),
)
