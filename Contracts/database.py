from aiopg.sa import create_engine


async def connection():
    engine = await create_engine(user='contracts_user',
                                 database='contracts',
                                 host='127.0.0.1',
                                 port=5432,
                                 password='contracts_user')
    return engine
