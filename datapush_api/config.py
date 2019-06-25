import socket


class Config:
    SDA_HOST = "0.0.0.0"
    SDA_PORT = 20000
    SDA_CONNECT = socket.gethostbyname(socket.gethostname())

    SERVICE_HOST = "0.0.0.0"
    SERVICE_PORT = 17000
