from service_api.database import *
from service_api.domain.models import payment
from datetime import datetime
from dateutil.parser import parse
import sqlalchemy as sa
from sqlalchemy.sql import column


async def filter_payments(query):
    engine = await connect_db()
    raw_data = []
    async with engine.acquire() as conn:
        selected_rows = await conn.execute(query)
        async for row in selected_rows:
            raw_data.append(row)
    return raw_data


async def get_response(fields, payment_id, contributor, start, finish, amount_min, amount_max):

    columns = [column(c) for c in fields]
    if payment_id[0]:
        query = sa.sql.select(columns, payment.c.id.in_(payment_id))
    elif contributor[0]:
        query = sa.sql.select(columns, payment.c.contributor.in_(contributor))
    else:

        query = (
            sa.sql.select(columns)
            .where(payment.c.date > start)
            .where(payment.c.date < finish)
            .where(payment.c.amount > float(amount_min))
            .where(payment.c.amount < float(amount_max))
        )

    raw_data = await filter_payments(query)
    return raw_data


async def get_transform_date_start(start_period):
    transform_start_day = parse(start_period).date()
    start = datetime.combine(transform_start_day, datetime.min.time())
    return start


async def get_transform_date_finish(end_period):
    transform_finish_day = parse(end_period).date()
    finish = datetime.combine(transform_finish_day, datetime.max.time())
    return finish


async def get_attributes_from_url(request):
    columns_payment = "id, amount, date, contributor, contract_id"
    fields = request.args.get("fields", columns_payment).replace(' ', '').split(',')
    payment_id = request.args.get("id", '').replace(' ', '').split(',')
    contributor = request.args.get("contributor", '').replace(' ', '').split(',')
    amount_min = request.args.get("amount_min", 0)
    amount_max = request.args.get("amount_max", 10 ** 10)
    start_period = request.args.get("start_period", "2016-06-29")
    end_period = request.args.get("end_period", str(datetime.now()))

    start_period = await get_transform_date_start(start_period)
    end_period = await get_transform_date_finish(end_period)
    raw_data = await get_response(fields, payment_id, contributor, start_period, end_period, amount_min, amount_max)
    return raw_data


async def create(json):
    engine = await connect_db()
    async with engine.acquire() as conn:
        for row in json.get('insert'):
            values = {
                "contributor": row["contributor"],
                "amount": row["amount"],
                "date": row["date"],
                "contract_id": row["contract_id"],
            }
            await conn.execute(payment.insert().values(values))


async def update(json):
    engine = await connect_db()
    async with engine.acquire() as conn:
        for row in json.get('update'):
            await conn.execute(
                payment.update()
                .where(payment.c.id == row["id"])
                .values(
                    contributor=row["contributor"],
                    amount=row["amount"],
                    date=row["date"],
                    contract_id=row["contract_id"],
                )
            )


async def delete(request):
    engine = await connect_db()
    async with engine.acquire() as conn:
        payment_id = request.args.get("id", '').replace(' ', '').split(',')
        for item in payment_id:
            await conn.execute(payment.delete().where(payment.c.id == item))


