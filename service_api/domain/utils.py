import logging

import aiohttp
import psycopg2
from marshmallow import ValidationError
from sqlalchemy.sql import text

from config import SDA_HOST, SDA_PORT, SERVICE_NAME, SERVICE_SOCKET
from constants import AVAILABLE_FILTERS, AVAILABLE_OPERATORS
from database import connection
from service_api.resource.forms import ContractSchema


async def get_params_from_get_request(get_request_url):
    url_params = (get_request_url
                  .replace(f"http://{SERVICE_SOCKET}/{SERVICE_NAME}", "")
                  .replace("%20", " ")
                  .replace("%27", "'")
                  .replace("%28", "(")
                  .replace("%29", ")")
                  )
    return url_params


async def validate_values(field_value):
    try:
        ContractSchema().load(field_value)
        return None
    except ValidationError as err:
        return err.messages


async def get_clause_for_query(url_params):

    list_of_clauses = []
    column_value = {}

    filter_argument = await find_filter_argument(url_params)
    operator_and_values = await define_operator_and_values(
                                url_params, filter_argument
                                                           )
    argument_operator = operator_and_values[0]
    argument_value = operator_and_values[1]

    try:
        if argument_value.startswith("("):
            string_of_arguments = argument_value[2:-2]
            list_of_arguments = string_of_arguments.split("','")
            for value in list_of_arguments:
                column_value[filter_argument] = value
                invalid_value = await validate_values(column_value)
                if invalid_value:
                    raise ValidationError(
                        message=f'Bad request{invalid_value}'
                                          )
        else:
            column_value[filter_argument] = argument_value[1:-1]
            invalid_value = await validate_values(column_value)
            if invalid_value:
                raise ValidationError(message=f'Bad request{invalid_value}')

        clause_text = f"{filter_argument} " \
            f"{AVAILABLE_OPERATORS.get(str(argument_operator))} " \
            f"{argument_value}"

        if "and" in url_params:
            urls_divided_by_and = url_params.split("and")
            for url in urls_divided_by_and:
                if "filter" not in url:
                    argument = await find_filter_argument_after_and(url)
                    operator_and_values = await define_operator_and_values(
                                                            url, argument
                                                                           )
                    operator = operator_and_values[0]
                    values = operator_and_values[1]
                    clause_text += f" and {argument} " \
                        f"{AVAILABLE_OPERATORS.get(str(operator))} {values}"
        clause = text(clause_text)
        list_of_clauses.append(clause)
        return list_of_clauses
    except ValidationError as err:
        return 400, err.messages


async def find_filter_argument(url_params):

    filter_expression_start = url_params.find("filter=")
    filter_expression_end = url_params.find(" ", filter_expression_start)

    filter_argument = (url_params[
                       filter_expression_start:filter_expression_end
                       ].split("="))[1]
    return filter_argument


async def find_filter_argument_after_and(url):
    filter_argument_start = url.find(" ")
    filter_argument_end = url.find(" ", filter_argument_start + 1)
    filter_argument = url[filter_argument_start + 1: filter_argument_end]
    return filter_argument


async def define_operator_and_values(url_params, filter_argument,
                                     start_search=0):

    symbol = AVAILABLE_FILTERS.get(str(filter_argument), " ")
    argument_position = url_params.find(filter_argument, start_search)
    operator_index_start = url_params.find(" ", argument_position)
    operator_index_end = url_params.find(" ", operator_index_start + 1)
    operator = url_params[operator_index_start + 1: operator_index_end]

    if operator != "in":

        value_start = url_params.find(symbol, operator_index_end)
        value_end = url_params.find(symbol, value_start + 1)
        value = url_params[value_start: value_end + 1]
    else:
        value_start = url_params.find("(", operator_index_end)
        value_end = url_params.find(")", value_start)
        value = f'({url_params[value_start + 1: value_end]})'
    return [operator, value]


async def query_to_db(query, flag='many'):

    try:
        engine = await connection()
        async with engine.acquire() as conn:
            selected_rows = await conn.execute(query)
            if flag == 'many':
                data = []
                async for row in selected_rows:
                    data.append(row)
                return data
            elif flag == 'one':
                async for row in selected_rows:
                    return row

    except (psycopg2.ProgrammingError,
            psycopg2.IntegrityError,
            psycopg2.InternalError,
            psycopg2.OperationalError):
        logging.error(f"OperationalError. Input parameters are not correct")
        return 404, 'Not found'
    except psycopg2.DataError:
        logging.error(f"DataError. Input parameters are not correct")
        return 400, 'Bad request'


async def get_service_payments():
    payments_socket = []
    sda_address = f"http://{SDA_HOST}:{SDA_PORT}/payments"

    async with aiohttp.ClientSession() as session:
        resp = await session.get(sda_address)
        decoded_socket = await resp.text()
        if decoded_socket == '/payments':
            return 404
        socket_list = decoded_socket.split(",")
        payments_socket.append(socket_list[0][2:-1])
        payments_socket.append(socket_list[1][2:-2])
        url = f"http://{payments_socket[0]}:{payments_socket[1]}/payments/" \
            f"contracts/?filter=contract_id%20eq%20"
        return url


async def filter_response_by_fields(fields, contracts):
    filtered_contracts = []
    for contract in contracts:
        filtered_contract = {}
        for item in contract.items():
            if item[0] in fields:
                filtered_contract[item[0]] = item[1]
        filtered_contracts.append(filtered_contract)
    return filtered_contracts


async def pagination_of_url_params(contract_ids_list):
    flag = True
    list_of_urls_params = []
    while flag:
        if len(contract_ids_list) <= 50:
            list_of_urls_params.append(contract_ids_list)
            flag = False
        elif len(contract_ids_list) > 50:
            list_of_three_items = contract_ids_list[0:50]
            list_of_urls_params.append(list_of_three_items)
            contract_ids_list = contract_ids_list[50:]
    return list_of_urls_params
