from datapush_api.api_v1 import app
from datapush_api.basic_views import register_on_sda
from datapush_api.config import Config


if __name__ == "__main__":
    app.add_task(register_on_sda)
    app.run(host=Config.SERVICE_HOST, port=Config.SERVICE_PORT)
