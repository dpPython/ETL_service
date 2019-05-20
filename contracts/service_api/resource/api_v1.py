from sanic import Sanic
from .views import Contracts
from .registration import SmokeResource, registration

app = Sanic()

app.add_route(SmokeResource.as_view(), '/')
app.add_route(Contracts.as_view(), '/contracts')
