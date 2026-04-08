from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.settings import get_db
from src.database.models import ProductTypeModel
from src.templates_config import templates

router = APIRouter(prefix="/product-types")


@router.get(path="/", response_class=HTMLResponse)
async def get_product_types(
        request: Request,
        db: AsyncSession = Depends(get_db),
        name: str | None = None
):
    query = select(ProductTypeModel)
    if name:
        query = query.where(ProductTypeModel.name.ilike(f"%{name}%"))

    result = await db.execute(query)
    product_types = result.scalars().all()

    return templates.TemplateResponse(
        "product_types.html",
        {
            "request": request,
            "product_types": product_types,
            "filter_name": name or ""
        }
    )


@router.get(path="/create/", response_class=HTMLResponse)
async def create_product_type_form(request: Request):
    return templates.TemplateResponse(
        "product_type_create.html",
        {"request": request, "form_data": {}}
    )


@router.post(path="/create/", response_class=HTMLResponse)
async def create_product_type(
        request: Request,
        name: str = Form(None),
        db: AsyncSession = Depends(get_db)
):
    if not name:
        return HTMLResponse(f"""
            <div style="
                background-color:#f8d7da;
                color:#721c24;
                padding:10px;
                border-radius:5px;
                margin-bottom:15px;
            ">
                ❌ Помилка: Поле name не може бути порожнім!
            </div>
            <a href="/product-types/create/">Назад до форми</a>
        """)
    stmt = insert(ProductTypeModel).values(name=name)
    await db.execute(stmt)
    await db.commit()

    return HTMLResponse(f"""
        <p>Product Type '{name}' успішно створено!</p>
        <a href="/product-types/create/">Створити ще</a>
    """)


@router.get(path="/update/{id}/", response_class=HTMLResponse)
async def update_product_type_form(
        request: Request,
        id: int,
        db: AsyncSession = Depends(get_db)
):
    product_type = await db.get(ProductTypeModel, id)

    return templates.TemplateResponse("product_type_update.html", {
        "request": request,
        "product_type": product_type
    })


@router.post(path="/update/{id}/", response_class=HTMLResponse)
async def update_product_type(
        request: Request,
        id: int,
        name: str | None = Form(None),
        db: AsyncSession = Depends(get_db)
):
    if not name:
        return HTMLResponse(f"""
            <div style="
                background-color:#f8d7da;
                color:#721c24;
                padding:10px;
                border-radius:5px;
                margin-bottom:15px;
            ">
                ❌ Помилка: Поле name не може бути порожнім!
            </div>
            <a href="/product-types/update/{id}">Назад до форми</a>
        """)
    stmt = (
        update(ProductTypeModel)
        .where(ProductTypeModel.id == id)
        .values(name=name)
    )
    await db.execute(stmt)
    await db.commit()

    return HTMLResponse(f"""
            <p>ProductType оновлено!</p>
            <a href="/product-types/">Назад до всіх product types</a>
        """)
