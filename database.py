from aiopg.sa import create_engine
from config import *


async def connection():
    engine = await create_engine(
                                 user=DB_USER,
                                 database=SERVICE_DB,
                                 host=DB_HOST,
                                 port=DB_PORT,
                                 password=DB_PASSWORD
                                 )
    return engine
