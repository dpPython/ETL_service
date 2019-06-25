from sanic import response
from datapush_api.domain.base_domain import BaseDomain
import json as non_sanic_json


async def general_request(contracts_url, payments_url):
    facts_and_dimensions = dict()

    res_contracts = await BaseDomain(url=contracts_url).get_instances()
    res_payments = await BaseDomain(url=payments_url).get_instances()

    facts_and_dimensions["facts"] = non_sanic_json.loads(
        res_payments.body.decode("utf-8")
    )
    facts_and_dimensions["dimensions"] = non_sanic_json.loads(
        res_contracts.body.decode("utf-8")
    )

    result = response.json(facts_and_dimensions)
    return result
