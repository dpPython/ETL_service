from sanic import Sanic

from service_api.resource.registration import SmokeResource
from service_api.resource.views import Contract, Contracts, PaymentsByContracts

app = Sanic()
app.config.RESPONSE_TIMEOUT = 300

app.add_route(SmokeResource.as_view(), '/')
app.add_route(Contracts.as_view(), '/contracts')
app.add_route(Contract.as_view(), '/contract/<contract_id>')
app.add_route(PaymentsByContracts.as_view(),
              '/payments_by_contracts/<contract_ids>')
