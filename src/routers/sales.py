from datetime import datetime

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy import select, func, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import PriceListModel
from src.database.settings import get_db
from src.database.models import SaleModel
from src.templates_config import templates

router = APIRouter(prefix="/sales")


@router.get(path="/", response_class=HTMLResponse)
async def get_sales(
        request: Request,
        db: AsyncSession = Depends(get_db),
        sale_date: str | None = None,
        payment_date: str | None = None
):
    query = select(SaleModel)
    if sale_date:
        query = query.where(func.date(SaleModel.sale_date) == sale_date)
    if payment_date:
        query = query.where(func.date(SaleModel.payment_date) == payment_date)

    result = await db.execute(query)
    sales = result.scalars().all()

    return templates.TemplateResponse(
        "sales.html",
        {
            "request": request,
            "sales": sales,
            "sale_date": sale_date or "",
            "payment_date": payment_date or ""
        }
    )


@router.get(path="/create/", response_class=HTMLResponse)
async def create_sale_form(request: Request, db: AsyncSession = Depends(get_db)):
    price_lists = (await db.execute(select(PriceListModel))).scalars().all()

    return templates.TemplateResponse("sale_create.html", {
        "request": request,
        "price_lists": price_lists,
        "error": None,
        "form_data": {}
    })


@router.post(path="/create/", response_class=HTMLResponse)
async def create_sale(
        request: Request,
        amount: int = Form(None),
        sale_date: datetime | None = Form(None),
        payment_date: datetime | None = Form(None),
        price_list_id: int | None = Form(None),
        db: AsyncSession = Depends(get_db)
):
    try:
        if amount <= 0:
            return HTMLResponse(f"""
                <div style="
                    background-color:#f8d7da;
                    color:#721c24;
                    padding:10px;
                    border-radius:5px;
                    margin-bottom:15px;
                ">
                    ❌ Помилка: Поле amount має бути > 0!
                </div>

                <a href="/sales/create/">Назад до форми</a>
            """)
        stmt = insert(SaleModel).values(
            amount=amount,
            sale_date=sale_date,
            payment_date=payment_date,
            price_list_id=price_list_id
        )
        await db.execute(stmt)
        await db.commit()

        return HTMLResponse(f"""
            <p>Sale '{amount}' успішно створено!</p>
            <a href="/sales/create/">Створити ще</a>
        """)

    except Exception:
        await db.rollback()
        return HTMLResponse(f"""
            <div style="
                background-color:#f8d7da;
                color:#721c24;
                padding:10px;
                border-radius:5px;
                margin-bottom:15px;
            ">
                ❌ Помилка: Поле amount не може бути порожнім!
            </div>

            <a href="/sales/create/">Назад до форми</a>
        """)


@router.get(path="/update/{id}/", response_class=HTMLResponse)
async def update_sale_form(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db)
):
    sale = await db.get(SaleModel, id)
    price_lists = (await db.execute(select(PriceListModel))).scalars().all()

    return templates.TemplateResponse("sale_update.html", {
        "request": request,
        "sale": sale,
        "price_lists": price_lists
    })


@router.post(path="/update/{id}/", response_class=HTMLResponse)
async def update_sale(
    request: Request,
    id: int,
    amount: int | None = Form(None),
    sale_date: datetime | None = Form(None),
    payment_date: datetime | None = Form(None),
    price_list_id: int | None = Form(None),
    db: AsyncSession = Depends(get_db)
):
    try:
        if amount <= 0:
            return HTMLResponse(f"""
                <div style="
                    background-color:#f8d7da;
                    color:#721c24;
                    padding:10px;
                    border-radius:5px;
                    margin-bottom:15px;
                ">
                    ❌ Помилка: Поле amount має бути > 0!
                </div>

                <a href="/sales/update/{id}/">Назад до форми</a>
            """)
        stmt = (
            update(SaleModel)
            .where(SaleModel.id == id)
            .values(
                amount=amount,
                sale_date=sale_date,
                payment_date=payment_date,
                price_list_id=price_list_id
            )
        )

        await db.execute(stmt)
        await db.commit()

        return HTMLResponse(f"""
            <p>Sale оновлено!</p>
            <a href="/sales/">Назад до всіх sales</a>
        """)

    except Exception:
        await db.rollback()
        return HTMLResponse(f"""
            <div style="
                background-color:#f8d7da;
                color:#721c24;
                padding:10px;
                border-radius:5px;
                margin-bottom:15px;
            ">
                ❌ Помилка: Поле amount не може бути порожнім!
            </div>

            <a href="/sales/update/{id}/">Назад до форми</a>
        """)
