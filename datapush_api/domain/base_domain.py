from sanic.response import json
from http import HTTPStatus
import aiohttp
import logging


class BaseDomain:
    def __init__(self, url):
        self.url = url

    async def get_instances(self):
        async with aiohttp.request(
                method="GET", url=self.url
        ) as service_response:
            try:
                result = await service_response.json()
            except Exception as exc:
                logging.error(exc)
                msg = "Got invalid type of response!"
                return json(f"Error: {msg}")
            else:
                if service_response.status == HTTPStatus.OK:
                    msg = f"Operation successful"
                    logging.info(msg)
                    return json(result)
                else:
                    msg = f"Got {service_response.status}"
                    logging.error(msg)
                    return json(f"Error: {msg}")
