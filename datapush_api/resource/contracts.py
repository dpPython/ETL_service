from sanic.views import HTTPMethodView
from sanic.response import text
from datapush_api.domain.base_domain import BaseDomain
from datapush_api.constants import (
    CONTRACTS_APP_NAME, SDA_UNREGISTERED_SERVICES_LIST
)
from datapush_api.validation.validator import validate_params
from datapush_api.basic_views import (
    restructure_params,
    get_service_socket
)


class Contracts(HTTPMethodView):
    async def get(self, request, contract_id=None, contracts_ids_list=None):
        service_url = await get_service_socket(CONTRACTS_APP_NAME)

        if service_url in SDA_UNREGISTERED_SERVICES_LIST:
            msg = f"Can not connect to '{CONTRACTS_APP_NAME.upper()}' service"
            return text(msg)

        params = await restructure_params(request.args)
        is_params_valid, validator_message = await validate_params(
            params, CONTRACTS_APP_NAME
        )

        if is_params_valid:
            service_url += request.url[request.url.find("/", 8):]
            result = await BaseDomain(
                url=service_url
            ).get_instances()

            return result
        else:
            return text(validator_message)
