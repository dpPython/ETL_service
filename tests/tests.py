import json

from service_api.resource.api_v1 import app


def test_smoke_get_returns_200():
    request, response = app.test_client.get('/')
    assert response.status == 200


def test_smoke_put_not_allowed():
    request, response = app.test_client.put('/')
    assert response.status == 405


def test_smoke_post_not_allowed():
    request, response = app.test_client.post('/')
    assert response.status == 405


def test_smoke_delete_not_allowed():
    request, response = app.test_client.post('/')
    assert response.status == 405


def test_contracts_get_returns_200():
    request, response = app.test_client.get('/contracts/')
    assert response.status == 200


def test_contracts_put_returns_200():
    data = [{
        "amount": 23400,
        "id": "a32d6557-1553-40c5-a60a-47832e643e4f",
        "title": "Contract-9999999",
        "executor": "Airbus Group",
        "start_date": "2010-07-09",
        "end_date": "2011-06-24",
        "customer": "Express Scripts Holding"
    },
     {
        "amount": 93600,
        "id": "f0ff9365-d1fd-4ee6-be2d-7c33cfd06475",
        "title": "Contract-8888888",
        "executor": "Airbus Group",
        "start_date": "2014-05-13",
        "end_date": "2015-04-28",
        "customer": "Carrefour"
            }]
    request, response = app.test_client.put(
                                            '/contracts/',
                                            data=json.dumps(data)
                                            )
    assert response.status == 200


def test_contracts_post_returns_200():
    data = [{
        "customer": "Honda1",
        "id": "580721d1-9611-4b23-aa3c-9c4458a58978",
        "amount": 200000000,
        "executor": "Brembo",
        "end_date": "2018-12-27T00:00:00+02:00",
        "start_date": "2019-12-27T00:00:00+02:00",
        "title": "Contract-800"
    },
     {
        "customer": "Acura",
        "id": "791d5831-4c78-42c9-babd-a5a81fe7faf3",
        "amount": 30000000,
        "executor": "Toyota Motor",
        "end_date": "2018-01-01T00:00:00+02:00",
        "start_date": "2019-01-01T00:00:00+02:00",
        "title": "Contract-801"
    }]
    request, response = app.test_client.post(
                                             '/contracts/',
                                             data=json.dumps(data)
                                             )
    assert response.status == 200


def test_contracts_delete_returns_200():
    params = {'id': 'c31d866e-7b88-4388-8df4-86283edbc341, '
                    '1546f9af-a268-49c0-9fbb-37c61be1b98c'}
    request, response = app.test_client.delete('/contracts', params=params)
    assert response.status == 200


def test_contract_get_returns_200():
    request, response = app.test_client.get(
        '/contract/6ce1bcf5-323d-4d62-a670-641f03eb4efe'
                                            )
    assert response.status == 200


def test_contract_put_returns_200():
    data = [{
            "customer": "Honda",
            "executor": "Brembo",
            "title": "Contract-9999",
            "end_date": "2018-12-27",
            "amount": 200000000,
            "start_date": "2019-12-27"
            }]
    request, response = app.test_client.put(
        '/contract/200d8bdc-c2e0-42be-9221-434ee791e63e',
        data=json.dumps(data)
                                            )
    assert response.status == 200


def test_contract_delete_returns_200():
    request, response = app.test_client.delete(
        '/contract/c31d866e-7b88-4388-8df4-86283edbc341'
                                               )
    assert response.status == 200
