from service_api.resource.contracts import PaymentsContract
from service_api.resource.payments import *
from service_api.resource.smoke import *
from sanic import Sanic


app = Sanic()

app.add_route(Smoke.as_view(), "/")
app.add_route(Smoke.as_view(), "/smoke")
app.add_route(Payments.as_view(), "payments/")  # PUT, POST, GET, DELETE

app.add_route(PaymentsContract.as_view(), "payments/contract/")  # GET

