from service_api.domain.models import contract
from database import connection
from config import SERVICE_SOCKET, SERVICE_NAME, SDA_PORT, SDA_HOST
import logging
import psycopg2
from sqlalchemy.sql import text
from service_api.resource.forms import ContractSchema
import aiohttp
from marshmallow import ValidationError



available_filters = {
                        "title": "'",
                        "amount": "'",
                        "start_date": "'",
                        "end_date": "'",
                        "id": "'",
                        "customer": "'",
                        "executor": "'"
                    }

available_operators = {
                        "eq": "=",
                        "ne": "!=",
                        "ge": ">=",
                        "gt": ">",
                        "le": "<=",
                        "lt": "<",
                        "in": "in",
                              }

'''handlers for GET request'''


async def get_params_from_get_request(get_request_url):
    url_params = (get_request_url
                  .replace(f"http://{SERVICE_SOCKET}/{SERVICE_NAME}", "")
                  .replace("%20", " ")
                  .replace("%27", "'")
                  )
    return url_params


async def get_clause_for_query(url_params):

    list_of_clauses = []
    column_value = {}

    filter_argument = await find_filter_argument(url_params)
    operator_and_values = await define_operator_and_values(url_params, filter_argument)
    argument_operator = operator_and_values[0]
    argument_value = operator_and_values[1]

    try:
        if argument_value.startswith("("):
            string_of_arguments = argument_value[2:-2]
            list_of_arguments = string_of_arguments.split("','")
            for value in list_of_arguments:
                column_value[filter_argument] = value
                valid_value = ContractSchema().load(column_value)
                if valid_value.errors:
                    raise ValidationError
        else:
            column_value[filter_argument] = argument_value[1:-1]
            valid_value = ContractSchema().load(column_value)
            if valid_value.errors:
                raise ValidationError(message=valid_value.errors)

        clause_text = f"{filter_argument} {available_operators.get(str(argument_operator))} {argument_value}"

        if "and" in url_params:
            urls_divided_by_and = url_params.split("and")
            for url in urls_divided_by_and:
                if "filter" not in url:
                    argument = await find_filter_argument_after_and(url)
                    operator_and_values = await define_operator_and_values(url, argument)
                    operator = operator_and_values[0]
                    values = operator_and_values[1]
                    clause_text += f" and {argument} {available_operators.get(str(operator))} {values}"
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


async def define_operator_and_values(url_params, filter_argument, start_search=0):

    symbol = available_filters.get(str(filter_argument), " ")
    argument_position = url_params.find(filter_argument, start_search)
    operator_index_start = url_params.find(" ", argument_position)
    operator_index_end = url_params.find(" ", operator_index_start + 1)
    operator = url_params[operator_index_start + 1: operator_index_end]

    if operator != "in":

        value_start = url_params.find(symbol, operator_index_end)
        value_end = url_params.find(symbol, value_start + 1)
        value = url_params[value_start: value_end + 1]
    else:
        value_start = url_params.find("%28", operator_index_end)
        value_end = url_params.find("%29", value_start)
        value = f'({url_params[value_start+3: value_end]})'
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

    except psycopg2.ProgrammingError:
        logging.error(f"ProgrammingError. Input parameters are not correct")
        return 404
    except psycopg2.InternalError:
        logging.error(f"InternalError. Input parameters are not correct")
        return 404
    except psycopg2.DataError:
        logging.error(f"DataError. Input parameters are not correct")
        return 'Bad request'
    except psycopg2.IntegrityError:
        logging.error(f"IntegrityError. Input parameters are not correct")
        return 404
    except psycopg2.OperationalError:
        logging.error(f"OperationalError. Input parameters are not correct")
        return 404


'''handlers for POST request'''


async def create_contracts(json):
    new_contracts = []
    for item in json:
        values_to_insert = {
                            "title": item["title"],
                            "amount": item["amount"],
                            "start_date": item["start_date"],
                            "end_date": item["end_date"],
                            "customer": item["customer"],
                            "executor": item["executor"]
                            }
        query = contract.insert().returning(
                                            contract.c.id,
                                            contract.c.title,
                                            contract.c.customer,
                                            contract.c.executor,
                                            contract.c.start_date,
                                            contract.c.end_date,
                                            contract.c.amount
                                            ).values(values_to_insert)
        new_contract = await query_to_db(query, flag='one')
        new_contracts.append(new_contract)
    return new_contracts

'''PUT request'''


async def update_contracts(json):

    updated_contracts = []
    for item in json:
        values_to_update = {
            "title": item["title"],
            "amount": item["amount"],
            "start_date": item["start_date"],
            "end_date": item["end_date"],
            "customer": item["customer"],
            "executor": item["executor"]
        }
        query = contract.update().returning(
            contract.c.id,
            contract.c.title,
            contract.c.customer,
            contract.c.executor,
            contract.c.start_date,
            contract.c.end_date,
            contract.c.amount
        ).where(contract.c.id == item["id"]).values(values_to_update)
        updated_contract = await query_to_db(query, flag='one')
        updated_contracts.append(updated_contract)

    return updated_contracts


async def check_existence_in_db(contract_ids):
    ids_of_existing_contracts = []
    ids_of_absence_contracts = []

    for contract_id in contract_ids:
        query = contract.select().where(contract.c.id == contract_id)
        contract_instance = await query_to_db(query, flag='one')
        if contract_instance:
            ids_of_existing_contracts.append(contract_instance)
        else:
            ids_of_absence_contracts.append(contract_id)
    return ids_of_existing_contracts, ids_of_absence_contracts


async def delete_contracts(contract_ids: list) -> dict:
    response_after_delete = {}
    ids_of_deleted_contracts = []
    ids_of_not_deleted_contracts = []

    for contract_id in contract_ids:
        exist, absent = await check_existence_in_db([contract_id])
        if absent:
            ids_of_not_deleted_contracts.append(contract_id)
        else:
            query = contract.delete().returning(contract.c.id).where(contract.c.id == contract_id)
            deleted_id = await query_to_db(query, flag='one')
            ids_of_deleted_contracts.append(deleted_id[0])

    if ids_of_deleted_contracts and ids_of_not_deleted_contracts:
        response_after_delete['Deleted contracts:'] = ids_of_deleted_contracts
        response_after_delete['There are no such contracts:'] = ids_of_not_deleted_contracts

    elif ids_of_deleted_contracts:
        response_after_delete['Deleted contracts:'] = ids_of_deleted_contracts

    else:
        response_after_delete['There are no such contracts:'] = ids_of_not_deleted_contracts

    return response_after_delete


async def get_contract_by_id(contract_id):
    query = contract.select().where(contract.c.id == contract_id)
    contract_instance = await query_to_db(query, flag='one')
    return contract_instance


async def update_contract_by_id(contract_id, json):
    for item in json:
        values_to_update = {
            "title": item["title"],
            "amount": item["amount"],
            "start_date": item["start_date"],
            "end_date": item["end_date"],
            "customer": item["customer"],
            "executor": item["executor"]
        }
        query = contract.update().returning(
            contract.c.id,
            contract.c.title,
            contract.c.customer,
            contract.c.executor,
            contract.c.start_date,
            contract.c.end_date,
            contract.c.amount
        ).where(contract.c.id == contract_id).values(values_to_update)
        updated_contract = await query_to_db(query, flag='one')

        return updated_contract


async def delete_contract_by_id(contract_id):
    response_after_delete = {}
    id_of_deleted_contract = ""
    id_of_not_deleted_contract = ""

    exist, absent = await check_existence_in_db([contract_id])
    if absent:
        id_of_not_deleted_contract += contract_id
    else:
        query = contract.delete().returning(contract.c.id).where(contract.c.id == contract_id)
        deleted_id = await query_to_db(query, flag='one')
        id_of_deleted_contract += deleted_id[0]

    if id_of_not_deleted_contract:
        response_after_delete['There are no such contract in database:'] = id_of_not_deleted_contract
    else:
        response_after_delete['ID of deleted contract:'] = id_of_deleted_contract

    return response_after_delete


async def get_service_payments():
    payments_socket = []
    sda_address = f"http://{SDA_HOST}:{SDA_PORT}/payments"
    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(sda_address)
            decoded_socket = await resp.text()
            socket_list = decoded_socket.split(",")
            payments_socket.append(socket_list[0][2:-1])
            payments_socket.append(socket_list[1][2:-2])
            url = f"http://{payments_socket[0]}:{payments_socket[1]}/payments"
            return url
    except Exception:
        return 404


async def send_get_request_to_payments(url, contract_ids):

    contract_ids_list = contract_ids.replace(" ", "").split(",")

    payments_by_contracts= {}

    for contract_id in contract_ids_list:
        params = {"filter": f'contract_id eq {str(contract_id)}'}
        try:
            async with aiohttp.ClientSession() as session:
                payments_by_contract = await session.get(url, params=params)
                payments_by_contracts[
                        f'Payments by contract {contract_id}'
                                      ] = payments_by_contract.json()   #responce_json.loads(payments_by_contract.body.decode("utf-8"))
        except ValueError:
            logging.error(f"ValueError. No payments with contract id {contract_id} founded")
            return 404

    return payments_by_contracts