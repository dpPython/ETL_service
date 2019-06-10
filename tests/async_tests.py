from service_api.domain.domain import *


async def test_get_params_from_get_request():
    get_request_url = "http://0.0.0.0:8007/contracts/?filter=id eq 'fdcdff55-93fa-4434-ad14-d66a0e77a964'"
    expected_result = "/?filter=id eq 'fdcdff55-93fa-4434-ad14-d66a0e77a964'"
    result = await get_params_from_get_request(get_request_url)
    assert result == expected_result


async def test_validate_values():
    field_value = {'id': 'e3f8a61b-9fab-445b-b8e3-61ddb4da5777'}
    result = await validate_values(field_value)
    expected_result = {}
    assert result == expected_result


async def test_validate_values_fail():
    field_value = {'id': 'f8a61b-9fab-445b-b8e3-61ddb4da5777'}
    result = await validate_values(field_value)
    expected_result = {'id': ['Not a valid UUID.']}
    assert result == expected_result


async def test_find_filter_argument_id():
    url_params = "/?filter=id eq 'fdcdff55-93fa-4434-ad14-d66a0e77a964'"
    result = await find_filter_argument(url_params)
    expected_result = 'id'
    assert result == expected_result


async def test_find_filter_argument_customer():
    url_params = "/?filter=customer eq 'Toyota'"
    result = await find_filter_argument(url_params)
    expected_result = 'customer'
    assert result == expected_result


async def test_find_filter_argument_amount():
    url_params = "/?filter=amount gt '52000'"
    result = await find_filter_argument(url_params)
    expected_result = 'amount'
    assert result == expected_result


async def test_find_filter_argument_amount_after_and():
    url_params = " amount gt '52000'"
    result = await find_filter_argument_after_and(url_params)
    expected_result = 'amount'
    assert result == expected_result


async def test_find_filter_argument_customer_after_and():
    url_params = " customer eg 'Acura'"
    result = await find_filter_argument_after_and(url_params)
    expected_result = 'customer'
    assert result == expected_result


async def test_define_operator_and_values_customer():
    url_params = "/?filter=customer eq 'Toyota'"
    filter_argument = 'customer'
    result = await define_operator_and_values(url_params, filter_argument)
    expected_result = ['eq', "'Toyota'"]
    assert result == expected_result


async def test_define_operator_and_values_id():
    url_params = "/?filter=id eq 'fdcdff55-93fa-4434-ad14-d66a0e77a964'"
    filter_argument = 'id'
    result = await define_operator_and_values(url_params, filter_argument)
    expected_result = ['eq', "'fdcdff55-93fa-4434-ad14-d66a0e77a964'"]
    assert result == expected_result


async def test_define_operator_and_values_amount():
    url_params = "/?filter=amount gt '52000'"
    filter_argument = 'amount'
    result = await define_operator_and_values(url_params, filter_argument)
    expected_result = ['gt', "'52000'"]
    assert result == expected_result


async def test_define_operator_and_values_executor_in():
    url_params = "/?filter=executor in %28'Carrefour', 'Costco', 'Airbus Group'%29"
    filter_argument = 'executor'
    result = await define_operator_and_values(url_params, filter_argument)
    expected_result = ['in', "('Carrefour', 'Costco', 'Airbus Group')"]
    assert result == expected_result


async def test_define_operator_and_values_title_in():
    url_params = "/?filter=title in %28'Contract-222', 'Contract-434'%29"
    filter_argument = 'title'
    result = await define_operator_and_values(url_params, filter_argument)
    expected_result = ['in', "('Contract-222', 'Contract-434')"]
    assert result == expected_result
