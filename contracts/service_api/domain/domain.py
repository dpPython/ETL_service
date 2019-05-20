from .models import Contract
from ..database  import connection 
from sqlalchemy import column
import sqlalchemy as sa


async def filter_contracts(query):
    engine = await connection()
    result = []
    async with engine.acquire() as conn:
        selected_rows = await conn.execute(query)
        async for row in selected_rows:
            result.append(row)
    return result


async def get_response(fields, contract_id, title, customer,
                       executor, start_period, end_period,
                       amount_min, amount_max
                       ):

    columns = [column(item) for item in fields]
    if contract_id[0]:
        query = sa.sql.select(columns, Contract.c.id.in_(contract_id))
    elif title[0]:
        query = sa.sql.select(columns, Contract.c.title.in_(title))
    elif customer[0]:
        query = sa.sql.select(columns, Contract.c.customer.in_(customer))
    elif executor[0]:
        query = sa.sql.select(columns, Contract.c.executor.in_(executor))
    else:
        query = (
            sa.sql.select(columns)
            .where(Contract.c.start_date < end_period)
            .where(Contract.c.end_date > start_period)
            .where(Contract.c.amount > float(amount_min))
            .where(Contract.c.amount < float(amount_max))
        )
    result = await filter_contracts(query)
    return result[0:30]


async def get_args_from_url(request):
    columns_contract = "id, title, amount, customer, executor, " \
                       "start_date, end_date"
    fields = request.args.get(
                              "fields", columns_contract
                              ).replace(' ', '').split(',')

    contract_id = request.args.get("id", '').replace(' ', '').split(',')
    title = request.args.get("title", '').replace(' ', '').split(',')
    customer = list(request.args.get("customer", '').split(','))
    executor = list(request.args.get("executor", '').split(','))
    amount_min = request.args.get("amount_min", 0)
    amount_max = request.args.get("amount_max", 10 ** 10)
    start_period = request.args.get("start_period", "1000-01-01")
    end_period = request.args.get("end_period", "3000-01-01")

    args = await get_response(fields, contract_id, title, customer, executor,
                              start_period, end_period, amount_min, amount_max
                              )
    return args


async def create(json):
    engine = await connection()
    async with engine.acquire() as conn:
        for item in json.get("insert", ""):
            values = {
                      "title": item["title"],
                      "amount": item["amount"],
                      "start_date": item["start_date"],
                      "end_date": item["end_date"],
                      "customer": item["customer"],
                      "executor": item["executor"]
                      }
            await conn.execute(Contract.insert().values(values))


async def update(json):
    engine = await connection()
    async with engine.acquire() as conn:
        for item in json.get("update", ""):
            await conn.execute(
                Contract.update()
                .where(Contract.c.id == item["id"])
                .values(
                        title=item['title'],
                        amount=item['amount'],
                        start_date=item['start_date'],
                        end_date=item['end_date'],
                        customer=item['customer'],
                        executor=item['executor']
                        )
                                )


async def delete(request):
    engine = await connection()
    async with engine.acquire() as conn:
        args = request.args.get("id", '').replace(' ', '').split(',')
        for contract_id in args:
            await conn.execute(Contract.delete().where(
                Contract.c.id == contract_id)
                                                        )
