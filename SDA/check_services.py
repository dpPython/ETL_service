import json
import requests
from time import sleep

while True:

    with open('file.json') as data_file:
        data = json.load(data_file)

    for i in list(data):
        if i == 'stub':
            continue

        try:
            response = requests.get(f'http://{data[i][0]}:{data[i][1]}')
        except requests.exceptions.ConnectionError:
            data.pop(i)

    with open('file.json', 'w') as data_file:
        data = json.dump(data, data_file)

    sleep(15)
