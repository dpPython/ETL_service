from sanic import response
from sanic.response import text
from sanic.views import HTTPMethodView

from .forms import ContractSchema
from ..domain.domain import get_args_from_url, create, update, delete


class Contracts(HTTPMethodView):
    async def get(self, request):
        contracts = await get_args_from_url(request)
        result = ContractSchema().dump(contracts, many=True)
        return response.json(result.data)

    async def post(self, request):
        await create(request.json)
        return text('Created')

    async def put(self, request):
        await update(request.json)
        return text("Updated")

    async def delete(self, request):
        await delete(request)
        return text("Deleted")
