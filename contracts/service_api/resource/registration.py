from sanic.views import HTTPMethodView
from sanic import response
import requests
import aiohttp
import logging


async def registration():
    # if requests.get(url="http://10.0.2.15:5001/").status_code == 200:
    sda = "http://10.4.169.216:5001/?name=contracts&ip=10.4.105.243&port=8007"
    #     r = requests.post(url=sda)


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
