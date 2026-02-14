from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import (
    SaleModel,
    PriceListModel,
    ProductTypeModel,
    ManufacturerModel
)
from src.database.settings import get_db

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")


@router.get("/tables", response_class=HTMLResponse)
async def show_tables(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ManufacturerModel))
    manufacturers = result.scalars().all()

    result = await db.execute(select(ProductTypeModel))
    product_types = result.scalars().all()

    result = await db.execute(select(PriceListModel))
    price_list = result.scalars().all()

    result = await db.execute(select(SaleModel))
    sales = result.scalars().all()

    return templates.TemplateResponse(
        "tables.html",
        {
            "request": request,
            "manufacturers": manufacturers,
            "product_types": product_types,
            "price_list": price_list,
            "sales": sales
        }
    )
