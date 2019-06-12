from sanic import response
from sanic.response import text
from sanic.views import HTTPMethodView
from service_api.domain.domain import *
from .forms import ContractSchema
from service_api.domain.models import contract


class Contracts(HTTPMethodView):

    async def get(self, request):
        url_params = await get_params_from_get_request(request.url)
        if 'filter' in url_params:
            list_of_clauses_for_query = await get_clause_for_query(url_params)
            if list_of_clauses_for_query[0] == 400:
                return response.json(status=400, body=f'Bad request! {list_of_clauses_for_query[1]}')
            query = contract.select().where(list_of_clauses_for_query[0])
            contracts = await query_to_db(query)
        else:
            contracts = await query_to_db(contract.select())
        if not contracts:
            return response.json(status=404, body="Not found! Contract doesn't exist")
        valid_data = ContractSchema().dump(contracts, many=True)
        return response.json(valid_data.data)

    async def post(self, request):
        new_contracts = await create_contracts(request.json)
        if new_contracts[0] == 400:
            return response.json(status=400, body=f'Bad request! {new_contracts[1]}')
        valid_new_contracts = ContractSchema().dump(new_contracts, many=True)
        return response.json(valid_new_contracts.data)

    async def put(self, request):
        updated_contracts = await update_contracts(request.json)
        if updated_contracts[0] == 400:
            return response.json(status=400, body=f'Bad request! {updated_contracts[1]}')
        valid_updated_contracts = ContractSchema().dump(updated_contracts, many=True)
        return response.json(valid_updated_contracts.data)

    async def delete(self, request):
        contract_ids = request.args.get("id", "").replace(" ", "").split(",")
        message_after_delete = await delete_contracts(contract_ids)
        return response.json(message_after_delete)


class Contract(HTTPMethodView):
    async def get(self, request, contract_id):
        desired_contract = await get_contract_by_id(contract_id)
        if desired_contract[0] == 400:
            return response.json(status=400, body=f'Bad request! {desired_contract[1]}')
        elif desired_contract[0] == 404:
            return response.json(status=404, body=f'{desired_contract[1]}')
        result = ContractSchema().dump(desired_contract)
        return response.json(result.data)

    async def put(self, request, contract_id):
        update_contract = await update_contract_by_id(contract_id, request.json)
        if update_contract[0] == 400:
            return response.json(status=400, body=f'Bad request! {update_contract[1]}')
        elif update_contract[0] == 404:
            return response.json(status=404, body=f'{update_contract[1]}')
        result = ContractSchema().dump(update_contract)
        return response.json(result.data)

    async def delete(self, request, contract_id):
        message_after_delete = await delete_contract_by_id(contract_id)
        if type(message_after_delete) == tuple:
            return response.json(status=400, body=f'Bad request! {message_after_delete[1]}')
        return response.json(message_after_delete)


class PaymentsByContract(HTTPMethodView):

    async def get(self, request, contract_ids):
        payments_url = await get_service_payments()
        if payments_url == 404:
            return text("Service payments is not available")
        elif payments_url != 404:
            payments_by_contracts = await send_get_request_to_payments(payments_url, contract_ids)
            return response.json(payments_by_contracts)

