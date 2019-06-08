from sanic import response
from sanic.response import text
from sanic.views import HTTPMethodView
from service_api.domain.domain import delete_contract_by_id, update_contract_by_id, get_contract_by_id, get_params_from_get_request, get_clause_for_query, query_to_db, create_contracts, update_contracts, delete_contracts #get_contracts, create_contracts, update_contracts, delete_contracts, get_contract_by_id
from .forms import ContractSchema
from service_api.domain.models import contract


class Contracts(HTTPMethodView):

    async def get(self, request):

        url_params = await get_params_from_get_request(request.url)
        if 'filter' in url_params:
            list_of_clauses_for_query = await get_clause_for_query(url_params)
            query = contract.select().where(list_of_clauses_for_query[0])
            contracts = await query_to_db(query)
            valid_data = ContractSchema().dump(contracts, many=True)
            return response.json(valid_data.data)
        else:
            contracts = await query_to_db(contract.select())
            if contracts != 404:
                valid_data = ContractSchema().dump(contracts, many=True)
                return response.json(valid_data)
        return text('Bad request')

    async def post(self, request):

        new_contracts = await create_contracts(request.json)
        valid_new_contracts = ContractSchema().dump(new_contracts, many=True)
        return response.json(valid_new_contracts.data)

    async def put(self, request):
        updated_contracts = await update_contracts(request.json)
        valid_updated_contracts = ContractSchema().dump(updated_contracts, many=True)
        return response.json(valid_updated_contracts.data)

    async def delete(self, request):
        contract_ids = request.args.get("id", "").replace(" ", "").split(",")
        message_after_delete = await delete_contracts(contract_ids)
        return response.json(message_after_delete)


class Contract(HTTPMethodView):
    async def get(self, request, contract_id):
        desired_contract = await get_contract_by_id(contract_id)
        result = ContractSchema().dump(desired_contract)
        return response.json(result.data)

    async def put(self, request, contract_id):
        update_contract = await update_contract_by_id(contract_id, request.json)
        result = ContractSchema().dump(update_contract)
        return response.json(result.data)

    async def delete(self, request, contract_id):
        message_after_delete = await delete_contract_by_id(contract_id)
        return response.json(message_after_delete)




