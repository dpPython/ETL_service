from sanic import Sanic
from Contracts.service_api.resource.views import Contracts
from Contracts.service_api.resource.registration import SmokeResource, registration

app = Sanic()

app.add_route(SmokeResource.as_view(), '/')
app.add_route(Contracts.as_view(), '/contracts')
