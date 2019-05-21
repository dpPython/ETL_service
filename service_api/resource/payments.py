from sanic import response
from service_api.domain.payments import *
from sanic.response import text
from sanic.views import HTTPMethodView
from service_api.forms import PaymentSchema


class Payments(HTTPMethodView):
    async def get(self, request):
        payments = await get_attributes_from_url(request)
        data = PaymentSchema().dump(payments, many=True)
        return response.json(data)

    async def post(self, request):
        await create(request.json)
        return text("I have created payment")

    async def put(self, request):
        await update(request.json)
        return text("I have updated payment")

    async def delete(self, request):
        await delete(request)
        return text("I have deleted payment")


