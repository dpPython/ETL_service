from sanic import Sanic
from service_api.resource.views import Contracts, Contract, PaymentsByContract
from service_api.resource.registration import SmokeResource

app = Sanic()
app.config.RESPONSE_TIMEOUT = 300

app.add_route(SmokeResource.as_view(), '/')                   # GET for Http.status OK
app.add_route(Contracts.as_view(), '/contracts')              # GET, POST, PUT, DELETE
app.add_route(Contract.as_view(), '/contract/<contract_id>')  # GET, PUT, DELETE for 1 item
app.add_route(PaymentsByContract.as_view(), '/payments_by_contract/<contract_ids>') #GET
