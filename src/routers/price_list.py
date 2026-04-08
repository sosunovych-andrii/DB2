from fastapi import APIRouter, Request, Depends, Query, Form
from fastapi.responses import HTMLResponse
from sqlalchemy import select, insert, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.constants import PAGE_SIZE
from src.database.models import ManufacturerModel, ProductTypeModel
from src.database.settings import get_db
from src.database.models import PriceListModel
from src.templates_config import templates

router = APIRouter(prefix="/price-list")


@router.get(path="/", response_class=HTMLResponse)
async def get_price_list(
        request: Request,
        db: AsyncSession = Depends(get_db),
        min_price: str | None = None,
        max_price: str | None = None,
        page: int = Query(1, ge=1, description="Номер сторінки")
):
    query = select(PriceListModel)

    if min_price not in (None, ""):
        try:
            query = query.where(PriceListModel.unit_price >= float(min_price))
        except ValueError:
            pass

    if max_price not in (None, ""):
        try:
            query = query.where(PriceListModel.unit_price <= float(max_price))
        except ValueError:
            pass

    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    offset = (page - 1) * PAGE_SIZE
    query = query.order_by(PriceListModel.id) \
        .offset(offset) \
        .limit(PAGE_SIZE)

    result = await db.execute(query)
    price_list = result.scalars().all()

    return templates.TemplateResponse(
        "price_list.html",
        {
            "request": request,
            "price_list": price_list,
            "min_price": min_price or "",
            "max_price": max_price or "",
            "page": page,
            "total_pages": (total + PAGE_SIZE - 1) // PAGE_SIZE if total else 1,
            "has_prev": page > 1,
            "has_next": page * PAGE_SIZE < total,
        }
    )


@router.get(path="/create/", response_class=HTMLResponse)
async def create_price_form(request: Request, db: AsyncSession = Depends(get_db)):
    manufacturers = (await db.execute(select(ManufacturerModel))).scalars().all()
    product_types = (await db.execute(select(ProductTypeModel))).scalars().all()

    return templates.TemplateResponse("price_list_create.html", {
        "request": request,
        "manufacturers": manufacturers,
        "product_types": product_types,
        "errors": [],
        "form_data": {}
    })


@router.post(path="/create/", response_class=HTMLResponse)
async def create_price(
        request: Request,
        unit_price: float | None = Form(None),
        manufacturer_id: int | None = Form(None),
        product_type_id: int | None = Form(None),
        db: AsyncSession = Depends(get_db)
):
    try:
        if unit_price <= 0:
            return HTMLResponse(f"""
                <div style="
                    background-color:#f8d7da;
                    color:#721c24;
                    padding:10px;
                    border-radius:5px;
                    margin-bottom:15px;
                ">
                    ❌ Помилка: Поле unit_price має бути > 0!
                </div>

                <a href="/price-list/create/">Назад до форми</a>
            """)
        stmt = insert(PriceListModel).values(
            unit_price=unit_price,
            manufacturer_id=manufacturer_id,
            product_type_id=product_type_id
        )
        await db.execute(stmt)
        await db.commit()
        return HTMLResponse(f"""
            <p>Price List '{unit_price}' успішно створено!</p>
            <a href="/price-list/create/">Створити ще</a>
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
                ❌ Помилка: Поле unit_price не може бути порожнім!
            </div>

            <a href="/price-list/create/">Назад до форми</a>
        """)


@router.get(path="/update/{id}/", response_class=HTMLResponse)
async def update_price_list_form(
        request: Request,
        id: int,
        db: AsyncSession = Depends(get_db)
):
    price = await db.get(PriceListModel, id)
    manufacturers = (await db.execute(select(ManufacturerModel))).scalars().all()
    product_types = (await db.execute(select(ProductTypeModel))).scalars().all()

    return templates.TemplateResponse("price_list_update.html", {
        "request": request,
        "price": price,
        "manufacturers": manufacturers,
        "product_types": product_types,
        "error": None
    })


@router.post(path="/update/{id}/", response_class=HTMLResponse)
async def update_price_list(
        request: Request,
        id: int,
        unit_price: float | None = Form(None),
        manufacturer_id: int | None = Form(None),
        product_type_id: int | None = Form(None),
        db: AsyncSession = Depends(get_db)
):
    try:
        if unit_price <= 0:
            return HTMLResponse(f"""
                <div style="
                    background-color:#f8d7da;
                    color:#721c24;
                    padding:10px;
                    border-radius:5px;
                    margin-bottom:15px;
                ">
                    ❌ Помилка: Поле unit_price має бути > 0!
                </div>

                <a href="/price-list/update/{id}/">Назад до форми</a>
            """)
        stmt = (
            update(PriceListModel)
            .where(PriceListModel.id == id)
            .values(
                unit_price=unit_price,
                manufacturer_id=manufacturer_id,
                product_type_id=product_type_id
            )
        )
        await db.execute(stmt)
        await db.commit()
        return HTMLResponse(f"""
                    <p>PriceList оновлено!</p>
                    <a href="/price-list/">Назад до price list</a>
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
                ❌ Помилка: Поле unit_price не може бути порожнім!
            </div>

            <a href="/price-list/update/{id}/">Назад до форми</a>
        """)
