from sanic import response
from sanic.response import text
from sanic.views import HTTPMethodView

from service_api.domain.services import (create_contracts,
                                         delete_contract_by_id,
                                         delete_contracts, get_contract_by_id,
                                         get_contracts,
                                         get_payments_by_contracts,
                                         update_contract_by_id,
                                         update_contracts,
                                         update_some_fields_of_contract_by_id,
                                         update_some_fields_of_contracts)
from service_api.domain.utils import get_service_payments
from service_api.resource.forms import ContractSchema


class Contracts(HTTPMethodView):

    async def get(self, request):
        contracts = await get_contracts(request)
        if contracts[0] == 400:
            return response.json(
                status=400,
                body=f'Bad request! {contracts[1]}'
                                 )
        elif contracts[0] == 404:
            return response.json(
                status=404,
                body="Not found! Contract doesn't exist")
        valid_data = ContractSchema().dump(contracts, many=True)
        return response.json(valid_data)

    async def post(self, request):
        new_contracts = await create_contracts(request.json)
        if new_contracts[0] == 400:
            return response.json(
                status=400,
                body=f'Bad request! {new_contracts[1]}'
                                 )
        valid_new_contracts = ContractSchema().dump(new_contracts, many=True)
        return response.json(valid_new_contracts)

    async def put(self, request):
        updated_contracts = await update_contracts(request.json)
        if updated_contracts[0] == 400:
            return response.json(
                status=400,
                body=f'Bad request! {updated_contracts[1]}'
                                 )
        valid_updated_contracts = ContractSchema().dump(
                                                        updated_contracts,
                                                        many=True
                                                        )
        return response.json(valid_updated_contracts)

    async def patch(self, request):
        updated_contracts = await update_some_fields_of_contracts(request.json)
        if updated_contracts[0] == 400:
            return response.json(
                status=400,
                body=f'Bad request! {updated_contracts[1]}'
                                 )
        elif updated_contracts[0] == 404:
            return response.json(
                status=404,
                body=f"Not found! {updated_contracts[1]}"
                                 )
        valid_updated_contracts = ContractSchema().dump(
                                                        updated_contracts,
                                                        many=True
                                                        )
        return response.json(valid_updated_contracts)

    async def delete(self, request):
        contract_ids = request.args.get("id", "").replace(" ", "").split(",")
        message_after_delete = await delete_contracts(contract_ids)
        return response.json(message_after_delete)


class Contract(HTTPMethodView):
    async def get(self, request, contract_id):
        desired_contract = await get_contract_by_id(contract_id)
        if desired_contract[0] == 400:
            return response.json(
                status=400,
                body=f'Bad request! {desired_contract[1]}'
                                 )
        elif desired_contract[0] == 404:
            return response.json(status=404, body=f'{desired_contract[1]}')
        result = ContractSchema().dump(desired_contract)
        return response.json(result)

    async def put(self, request, contract_id):
        updated_contract = await update_contract_by_id(
                                                      contract_id,
                                                      request.json
                                                      )
        if updated_contract[0] == 400:
            return response.json(
                status=400,
                body=f'Bad request! {updated_contract[1]}'
                                 )
        elif updated_contract[0] == 404:
            return response.json(status=404, body=f'{updated_contract[1]}')
        result = ContractSchema().dump(updated_contract)
        return response.json(result)

    async def patch(self, request, contract_id):
        updated_contract = await update_some_fields_of_contract_by_id(
                                                              contract_id,
                                                              request.json
                                                                      )
        if updated_contract[0] == 400:
            return response.json(
                status=400,
                body=f'Bad request! {updated_contract[1]}'
                                 )
        elif updated_contract[0] == 404:
            return response.json(status=404, body=f'{updated_contract[1]}')
        result = ContractSchema().dump(updated_contract)
        return response.json(result)

    async def delete(self, request, contract_id):
        message_after_delete = await delete_contract_by_id(contract_id)
        if type(message_after_delete) == tuple:
            return response.json(
                                 status=400,
                                 body=f'Bad request! {message_after_delete[1]}'
                                 )
        return response.json(message_after_delete)


class PaymentsByContract(HTTPMethodView):

    async def get(self, request, contract_ids):
        payments_url = await get_service_payments()
        if payments_url == 404:
            return text("Service payments is not available")
        payments_by_contracts = await get_payments_by_contracts(
                                            payments_url, contract_ids
                                                                )
        return response.json(payments_by_contracts)
