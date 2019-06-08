from sanic.views import HTTPMethodView
from sanic import response
import aiohttp
import logging
from config import *


async def registration():
    sda = f'http://{SDA_HOST}:{SDA_PORT}/?name={SERVICE_NAME}&ip={SERVICE_HOST}&port={SERVICE_PORT}'
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
