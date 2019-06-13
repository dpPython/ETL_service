from aiopg.sa import create_engine

from config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER, SERVICE_DB


async def connection():
    engine = await create_engine(
                                 user=DB_USER,
                                 database=SERVICE_DB,
                                 host=DB_HOST,
                                 port=DB_PORT,
                                 password=DB_PASSWORD
                                 )
    return engine
