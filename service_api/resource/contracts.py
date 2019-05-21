from sanic import response
from service_api.domain.contracts import *
from sanic.response import text
from sanic.views import HTTPMethodView
from service_api.forms import PaymentSchema


class PaymentsContract(HTTPMethodView):
    async def get(self, request):
        contract_id = request.args.get("id", '').replace(' ', '').split(',')
        contracts_url = await get_service_contracts()
        check_contracts = await send_request_contracts(contracts_url, contract_id)
        if check_contracts:
            payments = await get_contracts(check_contracts)
            data = PaymentSchema().dump(payments, many=True)
            return response.json(data)
        else:
            return text("Contracts not founded")
