import logging

import aiohttp
from sanic import response
from sanic.views import HTTPMethodView

from config import (SDA_HOST, SDA_PORT, SERVICE_HOST,
                    SERVICE_NAME, SERVICE_PORT)


async def registration():
    # sda = f'http://{SDA_HOST}:{SDA_PORT}/?name={SERVICE_NAME}&' \
    #       f'ip={SDA_CONNECT}&port={SERVICE_PORT}'
    sda = f'http://{SDA_HOST}:{SDA_PORT}/?name={SERVICE_NAME}&' \
        f'ip={SERVICE_HOST}&port={SERVICE_PORT}'
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(sda)

    except Exception as exc:
        logging.error(exc)


class SmokeResource(HTTPMethodView):
    def get(self, request):
        return response.json(
                             {'message': 'Service enabled'},
                             headers={'Service': 'Contracts'},
                             status=200
                              )
