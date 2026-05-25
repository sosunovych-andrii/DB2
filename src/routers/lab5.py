from fastapi import APIRouter
from starlette.requests import Request

from src.database.settings_mongodb import get_mongo
from src.templates_config import templates

router = APIRouter(prefix="/mdb")


@router.get("/query1/")
async def lab4_query1(request: Request):
    mongo_db = get_mongo()

    pipeline = [
        {
            "$lookup": {
                "from": "price_lists",
                "localField": "price_list_id",
                "foreignField": "id",
                "as": "price"
            }
        },
        {"$unwind": "$price"},

        {
            "$lookup": {
                "from": "product_types",
                "localField": "price.product_type_id",
                "foreignField": "id",
                "as": "type"
            }
        },
        {"$unwind": "$type"},

        {
            "$lookup": {
                "from": "manufacturers",
                "localField": "price.manufacturer_id",
                "foreignField": "id",
                "as": "man"
            }
        },
        {"$unwind": "$man"},

        {
            "$match": {
                "price.unit_price": {"$lte": 45},
                "type.name": {"$regex": ".*(Праск|Фен|Міксер).*", "$options": "i"}
            }
        },

        {
            "$addFields": {
                "final_price": {
                    "$cond": [
                        {"$lte": ["$amount", 15]},
                        {"$multiply": ["$price.unit_price", 1.03]},
                        "$price.unit_price"
                    ]
                }
            }
        },

        {
            "$addFields": {
                "total_cost": {"$multiply": ["$amount", "$final_price"]}
            }
        },

        {
            "$project": {
                "_id": 0,
                "product_type": "$type.name",
                "manufacturer": "$man.name",
                "price": "$final_price",
                "sale_date": 1,
                "amount": 1,
                "total_cost": 1
            }
        }
    ]

    data = list(mongo_db.sales.aggregate(pipeline))

    return templates.TemplateResponse(
        "mdb_query1.html",
        {"request": request, "data": data}
    )


@router.get("/query2/")
async def lab4_query2(request: Request):
    mongo_db = get_mongo()

    pipeline = [
        {"$lookup": {"from": "price_lists", "localField": "price_list_id", "foreignField": "id", "as": "price"}},
        {"$unwind": "$price"},
        {"$lookup": {"from": "product_types", "localField": "price.product_type_id", "foreignField": "id", "as": "type"}},
        {"$unwind": "$type"},
        {"$lookup": {"from": "manufacturers", "localField": "price.manufacturer_id", "foreignField": "id", "as": "man"}},
        {"$unwind": "$man"},

        {"$match": {
            "$or": [
                {"sale_date": {"$regex": "^2005-04"}},
                {"sale_date": {"$regex": "^2005-06"}},
                {"sale_date": {"$regex": "^2019-04"}},
                {"sale_date": {"$regex": "^2019-06"}}
            ]
        }},

        {"$addFields": {
            "full_name": {"$concat": ["$type.name", " ", "$man.name"]},
            "total_cost": {"$multiply": ["$amount", "$price.unit_price"]}
        }},

        {"$project": {
            "_id": 0,
            "full_product_name": "$full_name",
            "sale_date": 1,
            "amount": 1,
            "total_cost": {"$round": ["$total_cost", 2]}
        }},

        {"$sort": {"sale_date": 1}}
    ]

    data = list(mongo_db.sales.aggregate(pipeline))
    return templates.TemplateResponse("mdb_query2.html", {"request": request, "data": data})


@router.get("/query3/")
async def lab4_query3(request: Request):
    mongo_db = get_mongo()

    pipeline = [
        {"$lookup": {"from": "price_lists", "localField": "price_list_id", "foreignField": "id", "as": "price"}},
        {"$unwind": "$price"},
        {"$lookup": {"from": "product_types", "localField": "price.product_type_id", "foreignField": "id", "as": "type"}},
        {"$unwind": "$type"},
        {"$lookup": {"from": "manufacturers", "localField": "price.manufacturer_id", "foreignField": "id", "as": "man"}},
        {"$unwind": "$man"},

        {"$project": {
            "_id": 0,
            "manufacturer": "$man.name",
            "product_type": "$type.name",
            "unit_price": {"$round": ["$price.unit_price", 2]},
            "amount": 1,
            "sale_date": 1
        }},

        {"$sort": {"amount": -1}},
        {"$limit": 5}
    ]

    data = list(mongo_db.sales.aggregate(pipeline))
    return templates.TemplateResponse("mdb_query3.html", {"request": request, "data": data})
