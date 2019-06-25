from sanic.views import HTTPMethodView
from sanic.response import text


class Smoke(HTTPMethodView):
    def get(self, request):
        return text("Service DataPush is running!")
