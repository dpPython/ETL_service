import socket
from select import select
from urllib.parse import (urlparse, parse_qs)
import json

tasks = []

to_read = {}
to_write = {}
to_add = {}
to_open_data = {}

URLS = {
    '/': 'Hello client!',
    '/contracts': '/contracts',
    '/payments': '/payments',
    '/data_push': '/data_push',
}


def open_data():
    with open("file.json", "r") as read_file:
        global services
        services = json.load(read_file)

    yield ('open', 'data')


def add_services(method, query):
    if method == 'POST':
        if query['name'][0] in services:
            pass
        else:
            services['/' + query['name'][0]] = [query['ip'][0], query['port'][0]]
            with open('file.json', 'w') as write_file:
                json.dump(services, write_file)
    yield ('add', 'element')


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()

    while True:

        yield ('read', server_socket)
        client_socket, addr = server_socket.accept()

        print('Connection from', addr)

        tasks.append(open_data())
        tasks.append(client(client_socket))


def client(client_socket):
    yield ('read', client_socket)
    request = client_socket.recv(4096)

    if not request:
        client_socket.close()
    else:
        parsed = request.decode('utf-8').split(' ')
        method = parsed[0]
        url = parsed[1].lower()

        query = parse_qs(urlparse(url).query)

        tasks.append(add_services(method, query))

        if method != 'GET' or method != 'POST':
            headers, code = ('HTTP/1.1 405 Method not allowed \n\n', 405)
            body = f'<h1>Method not allowed</h1>'

        if url not in URLS:
            headers, code = ('HTTP/1.1 404 Not found \n\n', 404)
            body = f'<h1>Page not found</h1>'

        if (method == 'GET' or method == 'POST') and url in URLS:
            headers, code = ('HTTP/1.1 200 OK \n\n', 200)
            body = f'{services[URLS[url]] if url in services else URLS[url]}'

        response = (headers + body).encode()

        yield ('write', client_socket)
        client_socket.send(response)

    client_socket.close()


def event_loop():

    while any([tasks, to_read, to_write]):

        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)

            reason, sock = next(task)

            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task
            if reason == 'add':
                to_add[sock] = task
            if reason == 'open_data':
                to_open_data[sock] = task
        except StopIteration:
            print('Done')


tasks.append(server())
event_loop()
