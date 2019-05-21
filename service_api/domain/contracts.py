from service_api.database import *
from service_api.domain.models import payment
import aiohttp
import logging
from config import *


async def get_service_contracts():
    service_socket = []
    sda_address = f"http://{SDA_HOST}:{SDA_PORT}/contracts"
    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(sda_address)
    except Exception as exc:
        logging.error(exc)

    decoded_socket = await resp.text()
    socket_list = decoded_socket.split(",")
    service_socket.append(socket_list[0][2:-1])
    service_socket.append(socket_list[1][2:-2])
    url = f"http://{service_socket[0]}:{service_socket[1]}/contracts"
    return url


async def send_request_contracts(contracts_url, contract_id):

    array_id = []
    for item in contract_id:
        params = {"id": str(item)}
        try:
            async with aiohttp.ClientSession() as session:
                r = await session.get(contracts_url, params=params)
                if r.status == 200:
                    array_id.append(item)
        except Exception as exc:
            logging.error(exc)
    return array_id


async def get_contracts(contracts):
    engine = await connect_db()
    raw_data = []
    query = payment.select().where(payment.c.contract_id.in_(contracts))
    async with engine.acquire() as conn:
        selected_rows = await conn.execute(query)
        async for row in selected_rows:
            raw_data.append(row)
    return raw_data


