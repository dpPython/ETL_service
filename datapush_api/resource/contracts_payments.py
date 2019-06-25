from sanic.views import HTTPMethodView
from sanic.response import json
from datapush_api.domain.contracts_payments import general_request
from datapush_api.validation.validator import validate_params
from datapush_api.constants import (
    PAYMENTS_APP_NAME, CONTRACTS_APP_NAME, SDA_UNREGISTERED_SERVICES_LIST
)
from datapush_api.basic_views import (
    restructure_params, get_service_socket
)


class ContractsPayments(HTTPMethodView):
    async def get(self, request):
        service_contracts_url = await get_service_socket(CONTRACTS_APP_NAME)
        service_payments_url = await get_service_socket(PAYMENTS_APP_NAME)

        if service_contracts_url in SDA_UNREGISTERED_SERVICES_LIST:
            msg = f"Can not connect to '{CONTRACTS_APP_NAME.upper()}' service"
            return json(msg)
        if service_payments_url in SDA_UNREGISTERED_SERVICES_LIST:
            msg = f"Can not connect to '{PAYMENTS_APP_NAME.upper()}' service"
            return json(msg)

        params = await restructure_params(request.args)
        is_params_valid, validator_message = await validate_params(
            params, CONTRACTS_APP_NAME
        )

        if is_params_valid:
            service_contracts_url += "/contracts/" + request.url[request.url.find("/contracts-payments")+19:]
            service_payments_url += "/payments/contracts/" + request.url[request.url.find("/contracts-payments")+19:]
            service_payments_url = service_payments_url.replace("?filter=id", "?filter=contract_id")

            result = await general_request(
                contracts_url=service_contracts_url,
                payments_url=service_payments_url
            )
            return result
        else:
            return json(validator_message)
