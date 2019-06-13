from config import SERVICE_HOST, SERVICE_PORT
from service_api.resource.api_v1 import app
from service_api.resource.registration import registration

app.add_task(registration)

if __name__ == '__main__':
    app.run(host=SERVICE_HOST,
            port=SERVICE_PORT)
