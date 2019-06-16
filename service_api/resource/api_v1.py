from sanic import Sanic

from service_api.resource.registration import SmokeResource
from service_api.resource.views import Contract, Contracts, PaymentsByContracts

app = Sanic()
app.config.RESPONSE_TIMEOUT = 300

'''
Smoke resource with allowed method GET method
The main purpose is to indicate that the service is working.
'''
app.add_route(SmokeResource.as_view(), '/')

'''
Contracts resource with allowed methods GET, POST, PUT, PATCH, DELETE
The main purpose is to:
 - get all contracts in json
 - get contracts with specified parameters in json
 - create contracts with specified values and return that instances in json
 - replace data in specified contracts and return that instances in json
 - change some data in specified contract and return that instances in json
 - delete contracts with specified ids and return dict with values of
        deleted ids and ids that are absence in database if it is true.
'''
app.add_route(Contracts.as_view(), '/contracts')

'''
Contract resource with allowed methods GET, PUT, PATCH, DELETE
The same functionality as Contracts but only for one instance and except
of creating an instance of contract.
The id of instance must be specified in url.
'''
app.add_route(Contract.as_view(), '/contract/<contract_id>')

'''
PaymentsByContracts resource has only GET method.
 The main purpose is to get all payments in json with contract ids that are
 specified in url
'''
app.add_route(PaymentsByContracts.as_view(),
              '/payments_by_contracts/<contract_ids>')
