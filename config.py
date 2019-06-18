import socket

SERVICE_NAME = "contracts"
SERVICE_HOST = "0.0.0.0"
SERVICE_PORT = 7002
SERVICE_SOCKET = f'{SERVICE_HOST}:{SERVICE_PORT}'

SERVICE_DB = "contracts"
DB_HOST = "127.0.0.1"
DB_PORT = 5432
DB_USER = "contracts_user"
DB_PASSWORD = "contracts_user"

SDA_HOST = "0.0.0.0"
SDA_PORT = 7000
SDA_CONNECT = socket.gethostbyname(socket.gethostname())
