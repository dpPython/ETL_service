import datetime
from decimal import Decimal
from uuid import UUID

import psycopg2

from service_api.domain.domain import (define_operator_and_values,
                                       find_filter_argument,
                                       find_filter_argument_after_and,
                                       get_params_from_get_request,
                                       query_to_db, validate_values)


async def test_get_params_from_get_request():
    get_request_url = "http://0.0.0.0:8007/contracts/?filter=id " \
                      "eq 'fdcdff55-93fa-4434-ad14-d66a0e77a964'"
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
    url_params = "/?filter=executor in %28'Carrefour', " \
                 "'Costco', 'Airbus Group'%29"
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


async def test_query_to_db():
    query = "SELECT contract.id, contract.title, contract.amount, " \
            "contract.start_date, contract.end_date, contract.customer, " \
            "contract.executor FROM contract WHERE id" \
            " = 'fdcdff55-93fa-4434-ad14-d66a0e77a964'"
    result = await query_to_db(query)
    expected_result = [
        (UUID('fdcdff55-93fa-4434-ad14-d66a0e77a964'), 'Contract-210',
         Decimal('52000.0'), datetime.datetime(
            2012, 2, 1, 0, 0,
            tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=120, name=None)),
         datetime.datetime(
             2013, 1, 16, 0, 0,
             tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=120, name=None)),
         'Freddie Mac', 'Airbus Group')
                       ]
    assert result == expected_result


async def test_query_to_db_flag_one():
    query = "SELECT contract.id, contract.title, contract.amount, " \
            "contract.start_date, contract.end_date, contract.customer, " \
            "contract.executor FROM contract WHERE contract.id = " \
            "'f9cacfb4-0cde-42cc-8a94-ba90009d5cec'"
    result = await query_to_db(query, flag='one')
    expected_result = (UUID('f9cacfb4-0cde-42cc-8a94-ba90009d5cec'),
                       'Contract-83', Decimal('26600.0'), datetime.datetime(
        2010, 9, 11, 0, 0,
        tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)
                                                                            ),
                       datetime.datetime(
        2011, 8, 27, 0, 0,
        tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)
                                         ),
                       'Berkshire Hathaway', 'Airbus Group')
    assert result == expected_result
