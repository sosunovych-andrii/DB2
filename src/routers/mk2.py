from fastapi import APIRouter
from starlette.requests import Request

from src.database.settings_mongodb import get_mongo
from src.templates_config import templates

router = APIRouter(prefix="/mk2")


@router.get("/query1/")
async def lab6_query(request: Request):
    mongo_db = get_mongo()

    pipeline = [
        {
            "$lookup": {
                "from": "distributors",
                "localField": "distributor_code",
                "foreignField": "code",
                "as": "distributor"
            }
        },
        {"$unwind": "$distributor"},

        {
            "$match": {
                "order_date": {
                    "$gte": "2004-04-01",
                    "$lt": "2004-7-01"
                }
            }
        },

        {"$unwind": "$contents"},

        {
            "$addFields": {
                "unit_price": {
                    "$cond": {
                        "if": {"$eq": ["$distributor.country", "Великобританія"]},
                        "then": {"$multiply": ["$contents.price", 1.045]},
                        "else": "$contents.price"
                    }
                }
            }
        },

        {
            "$addFields": {
                "cost": {
                    "$multiply": ["$unit_price", "$contents.quantity"]
                }
            }
        },

        {
            "$project": {
                "_id": 0,
                "Номер замовлення": "$order_id",
                "Назва дистріб'ютора": "$distributor.name",
                "Адреса дистріб'ютора": "$distributor.address",
                "Дата замовлення": "$order_date",
                "Дата сплати": "$payment_date",
                "Кількість": "$contents.quantity",
                "Вартість": {"$round": ["$cost", 2]}
            }
        },

        {"$sort": {"Назва дистріб'ютора": 1}}
    ]

    data = list(mongo_db.orders.aggregate(pipeline))

    return templates.TemplateResponse(
        "mk2_query1.html",
        {"request": request, "data": data}
    )
