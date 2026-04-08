from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.settings import get_db
from src.database.models import ManufacturerModel
from src.templates_config import templates

router = APIRouter(prefix="/manufacturers")


@router.get(path="/", response_class=HTMLResponse)
async def get_manufacturers(
        request: Request,
        db: AsyncSession = Depends(get_db),
        name: str | None = None
):
    query = select(ManufacturerModel)
    if name:
        query = query.where(ManufacturerModel.name.ilike(f"%{name}%"))
    result = await db.execute(query)
    manufacturers = result.scalars().all()

    return templates.TemplateResponse(
        "manufacturers.html",
        {
            "request": request,
            "manufacturers": manufacturers,
            "filter_name": name or ""
        }
    )


@router.get(path="/create/", response_class=HTMLResponse)
async def create_manufacturer_form(request: Request):
    return templates.TemplateResponse(
        "manufacturer_create.html",
        {"request": request, "form_data": {}}
    )


@router.post(path="/create/", response_class=HTMLResponse)
async def create_manufacturer(
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
            <a href="/manufacturers/create/">Назад до форми</a>
        """)
    stmt = insert(ManufacturerModel).values(name=name)
    await db.execute(stmt)
    await db.commit()

    return HTMLResponse(f"""
        <p>Manufacturer '{name}' успішно створено!</p>
        <a href="/manufacturers/create/">Створити ще</a>
    """)


@router.get(path="/update/{id}/", response_class=HTMLResponse)
async def update_manufacturer_form(
        request: Request,
        id: int,
        db: AsyncSession = Depends(get_db)
):
    manufacturer = await db.get(ManufacturerModel, id)

    return templates.TemplateResponse("manufacturer_update.html", {
        "request": request,
        "manufacturer": manufacturer
    })


@router.patch(path="/update/{id}/", response_class=HTMLResponse)
async def update_manufacturer(
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
            <a href="/manufacturers/update/{id}">Назад до форми</a>
        """)
    stmt = (
        update(ManufacturerModel)
        .where(ManufacturerModel.id == id)
        .values(name=name)
    )
    await db.execute(stmt)
    await db.commit()

    return HTMLResponse(f"""
            <p>Manufacturer оновлено!</p>
            <a href="/manufacturers/">Назад до всіх manufacturers</a>
        """)
