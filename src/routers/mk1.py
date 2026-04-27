from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.mk1 import (
    FirmModel,
    OrderModel,
    ProductModel,
    OrderContentModel
)
from src.database.settings import get_db
from src.templates_config import templates

router = APIRouter()


# Замовлення за 3 квартал + пошук по фірмі
@router.get("/query1", response_class=HTMLResponse)
async def query1(
    request: Request,
    firm_name: str = Query(default=""),
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(
            OrderModel.id,
            ProductModel.name,
            FirmModel.name,
            OrderContentModel.quantity,
            ProductModel.price,
            (
                ProductModel.price *
                OrderContentModel.quantity *
                func.if_(
                    OrderContentModel.quantity > 10,
                    0.955,
                    1
                )
            ).label("total")
        )
        .join(OrderContentModel, OrderModel.id == OrderContentModel.order_id)
        .join(ProductModel, ProductModel.id == OrderContentModel.product_id)
        .join(FirmModel, FirmModel.id == OrderModel.firm_id)
        .where(
            and_(
                func.month(OrderModel.order_date).between(7, 9),
                FirmModel.name.ilike(f"{firm_name}%")
            )
        )
        .order_by(FirmModel.name, ProductModel.name)
    )

    result = await db.execute(stmt)

    return templates.TemplateResponse("query1.html", {
        "request": request,
        "rows": result.all()
    })


# Кількість замовлень між датами
@router.get("/query2", response_class=HTMLResponse)
async def query2(
    request: Request,
    date_from: str = Query(default=None),
    date_to: str = Query(default=None),
    db: AsyncSession = Depends(get_db)
):
    count = None

    if date_from and date_to:
        stmt = (
            select(func.count(OrderModel.id))
            .where(OrderModel.order_date.between(date_from, date_to))
        )
        result = await db.execute(stmt)
        count = result.scalar()

    return templates.TemplateResponse("query2.html", {
        "request": request,
        "count": count
    })


# Товари, які НЕ замовляла фірма "Impression"
@router.get("/query3", response_class=HTMLResponse)
async def query3(request: Request, db: AsyncSession = Depends(get_db)):

    subq = (
        select(OrderContentModel.product_id)
        .join(OrderModel)
        .join(FirmModel)
        .where(FirmModel.name == 'Impression')
    )

    stmt = (
        select(ProductModel)
        .where(~ProductModel.id.in_(subq))
    )

    result = await db.execute(stmt)

    return templates.TemplateResponse("query3.html", {
        "request": request,
        "products": result.scalars().all()
    })
