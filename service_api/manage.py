from service_api.resource.api_v1 import app
from service_api.resource.smoke import notification
from config import *

if __name__ == "__main__":
    app.add_task(notification())
    app.run(host=SERVICE_HOST, port=SERVICE_PORT, debug=True)
