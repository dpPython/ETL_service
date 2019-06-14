import logging

import aiohttp
from marshmallow import ValidationError
from sanic.exceptions import NotFound

from service_api.domain.models import contract
from service_api.domain.utils import (get_clause_for_query,
                                      get_params_from_get_request, query_to_db,
                                      validate_values)


async def get_contracts(request):
    url_params = await get_params_from_get_request(request.url)
    if 'filter' in url_params:
        list_of_clauses_for_query = await get_clause_for_query(url_params)
        if list_of_clauses_for_query[0] == 400:
            return 400, list_of_clauses_for_query[1]
        query = contract.select().where(list_of_clauses_for_query[0])
        contracts = await query_to_db(query)
    else:
        query = contract.select()
        contracts = await query_to_db(query)
    if not contracts:
        return 404, "Not found! Contract doesn't exist"
    return contracts


async def create_contracts(json):
    new_contracts = []
    required_field_names = {
        'title', 'amount', 'start_date', 'end_date',
        'customer', 'executor'
                            }
    try:
        for item in json:
            field_names_in_request = set(item.keys())
            if not required_field_names.issubset(field_names_in_request):
                raise ValidationError(
                    message='Not all required values in body'
                                      )
            values_to_insert = {
                                "title": item["title"],
                                "amount": item["amount"],
                                "start_date": item["start_date"],
                                "end_date": item["end_date"],
                                "customer": item["customer"],
                                "executor": item["executor"]
                                }
            invalid_values = await validate_values(values_to_insert)
            if invalid_values:
                raise ValidationError(message=invalid_values)

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
    except ValidationError as err:
        return 400, err.messages


async def update_contracts(json):

    updated_contracts = []
    required_field_names = {
        'title', 'amount', 'start_date', 'end_date',
        'customer', 'executor'
    }
    try:
        for item in json:
            field_names_in_request = set(item.keys())
            if not required_field_names.issubset(field_names_in_request):
                raise ValidationError(
                    message='Not all required values in body'
                                      )
            values_to_update = {
                "id": item["id"],
                "title": item["title"],
                "amount": item["amount"],
                "start_date": item["start_date"],
                "end_date": item["end_date"],
                "customer": item["customer"],
                "executor": item["executor"]
            }
            invalid_values = await validate_values(values_to_update)
            if invalid_values:
                raise ValidationError(message=invalid_values)
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
    except ValidationError as err:
        return 400, err.messages


async def update_some_fields_of_contracts(json):
    updated_contracts = []
    try:
        for item in json:
            values_to_update = item
            values_to_validate = values_to_update.copy()
            invalid_values = await validate_values(values_to_validate)
            if invalid_values:
                raise ValidationError(message=invalid_values)
            absence_in_db = await check_existence_in_db([item.get('id')])
            if absence_in_db[1]:
                raise NotFound(message='There are no contracts with such id')
            del values_to_update["id"]
            query = contract.update().returning(
                contract.c.id,
                contract.c.title,
                contract.c.customer,
                contract.c.executor,
                contract.c.start_date,
                contract.c.end_date,
                contract.c.amount
            ).where(contract.c.id == values_to_validate.get('id')).values(values_to_update)
            updated_contract = await query_to_db(query, flag="one")
            updated_contracts.append(updated_contract)

        return updated_contracts
    except ValidationError as err:
        return 400, err.messages
    except NotFound as err:
        return 404, err


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
            query = contract.delete().returning(contract.c.id).where(
                                        contract.c.id == contract_id
                                                                     )
            deleted_id = await query_to_db(query, flag='one')
            ids_of_deleted_contracts.append(deleted_id[0])
    if ids_of_deleted_contracts and ids_of_not_deleted_contracts:
        response_after_delete['Deleted contracts:'] = ids_of_deleted_contracts
        response_after_delete[
            'There are no such contracts:'
                              ] = ids_of_not_deleted_contracts
    elif ids_of_deleted_contracts:
        response_after_delete['Deleted contracts:'] = ids_of_deleted_contracts
    else:
        response_after_delete[
            'There are no such contracts:'
                              ] = ids_of_not_deleted_contracts
    return response_after_delete


async def get_contract_by_id(contract_id):
    try:
        invalid_contract_id = await validate_values({'id': contract_id})
        if invalid_contract_id:
            raise ValidationError(message=invalid_contract_id)
        query = contract.select().where(contract.c.id == contract_id)
        contract_instance = await query_to_db(query, flag='one')
        if not contract_instance:
            raise NotFound(
                message='Not found! There are no contracts with such id'
                           )
        return contract_instance

    except ValidationError as err:
        return 400, f'Bad request! {err.messages}'
    except NotFound as err:
        return err.status_code, err.args


async def update_contract_by_id(contract_id, json):
    required_field_names = {
        'title', 'amount', 'start_date', 'end_date',
        'customer', 'executor'
                            }
    try:
        for item in json:
            field_names_in_request = set(item.keys())
            if not required_field_names.issubset(field_names_in_request):
                raise ValidationError(
                    message='Not all required values in body'
                                      )
            values_to_update = {
                "title": item["title"],
                "amount": item["amount"],
                "start_date": item["start_date"],
                "end_date": item["end_date"],
                "customer": item["customer"],
                "executor": item["executor"]
            }
            values_to_validate = values_to_update.copy()
            values_to_validate['id'] = contract_id
            invalid_values = await validate_values(values_to_validate)
            if invalid_values:
                raise ValidationError(message=invalid_values)
            absence_in_db = await check_existence_in_db([contract_id])
            if absence_in_db[1]:
                raise NotFound(
                    message='Not found! There are no contracts with such id'
                               )
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
    except ValidationError as err:
        return 400, f'Bad request! {err.messages}'
    except NotFound as err:
        return err.status_code, err.args


async def update_some_fields_of_contract_by_id(contract_id, json):
    try:
        for item in json:
            values_to_update = item
            values_to_validate = values_to_update.copy()
            values_to_validate['id'] = contract_id
            invalid_values = await validate_values(values_to_validate)
            if invalid_values:
                raise ValidationError(message=invalid_values)
            absence_in_db = await check_existence_in_db([contract_id])
            if absence_in_db[1]:
                raise NotFound(
                    message='Not found! There are no contracts with such id'
                               )
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
    except ValidationError as err:
        return 400, f'Bad request! {err.messages}'
    except NotFound as err:
        return err.status_code, err.args


async def delete_contract_by_id(contract_id):
    try:
        invalid_contract_id = await validate_values({'id': contract_id})
        if invalid_contract_id:
            raise ValidationError(message=invalid_contract_id)
        response_after_delete = {}
        id_of_deleted_contract = ""
        id_of_not_deleted_contract = ""

        exist, absent = await check_existence_in_db([contract_id])
        if absent:
            id_of_not_deleted_contract += contract_id
        else:
            query = contract.delete().returning(contract.c.id).where(
                                        contract.c.id == contract_id
                                                                     )
            deleted_id = await query_to_db(query, flag='one')
            id_of_deleted_contract += deleted_id[0]

        if id_of_not_deleted_contract:
            response_after_delete[
                'There are no such contract in database:'
                                  ] = id_of_not_deleted_contract
        else:
            response_after_delete[
                'ID of deleted contract:'
                                  ] = id_of_deleted_contract

        return response_after_delete
    except ValidationError as err:
        return 400, err.messages


async def get_payments_by_contracts(url, contract_ids):
    contract_ids_list = contract_ids.replace(" ", "").split(",")
    payments_by_contracts = {}
    for contract_id in contract_ids_list:
        url_with_contract_id = f"{url}%27{contract_id}%27"
        try:
            async with aiohttp.ClientSession() as session:
                payments_by_contract = await session.get(url_with_contract_id)
                if payments_by_contract.content_type == 'text/plain':
                    data = 'Incorrect input of contract_id '
                else:
                    data = await payments_by_contract.json()
                    if not data:
                        data = 'There are no payments by this contract'
                payments_by_contracts[
                        f'Payments by contract {contract_id}'
                                      ] = data
        except ValueError:
            logging.error(f"ValueError. No payments with contract id "
                          f"{contract_id} founded")
            return 404
    return payments_by_contracts
