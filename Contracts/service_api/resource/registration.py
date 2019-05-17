from sanic.views import HTTPMethodView
from sanic import response
import aiohttp
import logging


async def registration():
    sda = "http://10.4.105.222:5004/?name=contracts&ip=10.4.105.222&port=8007"
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
