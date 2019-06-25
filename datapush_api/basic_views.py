from datapush_api.constants import *
from http import HTTPStatus
import aiohttp
import logging


async def register_on_sda(request):
    try:
        async with aiohttp.ClientSession() as session:
            sda_response = await session.get(SDA_ADDRESS)

            if sda_response.status == HTTPStatus.OK:
                sda_response = await session.post(url=REGISTRATION_URL)

                if sda_response.status == HTTPStatus.OK:
                    logging.info("successful registration")
    except Exception as exc:  # ConnectionRefusedError not working
        logging.error(exc)


async def get_service_socket(service_name):
    service_socket = []
    sda_address = f"{SDA_ADDRESS}/{service_name}"
    try:
        async with aiohttp.ClientSession() as session:
            sda_response = await session.get(sda_address)
    except Exception as exc:
        logging.error(exc)
        return f"/{service_name}"
    else:
        if sda_response.status == HTTPStatus.OK:
            decoded_response = await sda_response.text()
            raw_ip_port_list = decoded_response.split(",")

            if raw_ip_port_list[0] in SDA_UNREGISTERED_SERVICES_LIST:
                msg = f"Service {service_name} is unavailable"
                logging.error(msg)
                return f"/{service_name}"
            else:
                msg = f"Operation successful"
                logging.info(msg)

                service_socket.append(raw_ip_port_list[0][2:-1])
                service_socket.append(raw_ip_port_list[1][2:-2])

                url = f"http://{service_socket[0]}:{service_socket[1]}"
                return url

        msg = f"SDA is unavailable"
        logging.error(msg)
        return f"/{service_name}"


async def restructure_params(args):
    params = {}
    for key in args:
        params[key] = args[key][0]
    return params
