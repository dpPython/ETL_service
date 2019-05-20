from aiopg.sa import create_engine


async def connection():
    engine = await create_engine(user='postgres',
                                 database='contracts',
                                 host='192.168.1.113',
                                 port=2348,
                                 password='postgres')
    return engine
