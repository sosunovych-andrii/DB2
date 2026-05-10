from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.settings_lab4 import get_db
from src.templates_config import templates

router = APIRouter(prefix="/lab4")


@router.get(path="/query1/", response_class=HTMLResponse)
async def query1(
    request: Request,
    db: AsyncSession = Depends(get_db)
):

    sql = text("""
        SELECT 
            dtt.name AS type_name,
            dfv.name AS firm_name,

            IF(
                rt.amount <= 15,
                pt.price * 1.03,
                pt.price
            ) AS sale_price,

            rt.date_realization AS date_realization,

            IF(
                rt.amount <= 15, 
                (pt.price * 1.03) * rt.amount,
                pt.price * rt.amount
            ) AS total_price

        FROM dovidnyk_typiv_tovariv AS dtt

        INNER JOIN preyskurant_tovariv AS pt
            ON pt.id_type_tovar = dtt.id

        INNER JOIN dovidnyk_firmu_vyrobnyka AS dfv
            ON dfv.id = pt.id_firm

        INNER JOIN realizatsia_tovariv AS rt
            ON rt.id_preyskurant = pt.id

        WHERE 
            dtt.name IN (:type1, :type2)
            AND pt.price <= :max_price
    """)

    result = await db.execute(
        sql,
        {
            "type1": "міксер",
            "type2": "фен",
            "max_price": 45
        }
    )

    return templates.TemplateResponse(
        "lab4_query1.html",
        {
            "request": request,
            "rows": result.mappings().all()
        }
    )


@router.get(path="/query2/", response_class=HTMLResponse)
async def query2(
    request: Request,
    db: AsyncSession = Depends(get_db)
):

    sql = text("""
        SELECT
            CONCAT(dtt.name, ' - ', dfv.name) AS full_name,

            rt.date_realization AS date_realization,

            rt.amount AS amount,

            IF(
                rt.amount <= 15, 
                (pt.price * 1.03) * rt.amount,
                pt.price * rt.amount
            ) AS total_price

        FROM dovidnyk_typiv_tovariv AS dtt

        INNER JOIN preyskurant_tovariv AS pt
            ON pt.id_type_tovar = dtt.id

        INNER JOIN dovidnyk_firmu_vyrobnyka AS dfv
            ON dfv.id = pt.id_firm

        INNER JOIN realizatsia_tovariv AS rt
            ON rt.id_preyskurant = pt.id

        WHERE
            YEAR(rt.date_realization) = :year
            AND MONTH(rt.date_realization) IN (:month1, :month2)
    """)

    result = await db.execute(
        sql,
        {
            "year": 2019,
            "month1": 4,
            "month2": 6
        }
    )

    return templates.TemplateResponse(
        "lab4_query2.html",
        {
            "request": request,
            "rows": result.mappings().all()
        }
    )


@router.get(path="/query3/", response_class=HTMLResponse)
async def query3(
    request: Request,
    db: AsyncSession = Depends(get_db)
):

    sql = text("""
        SELECT 
            dfv.name AS firm_name,

            dtt.name AS type_name,

            IF(
                rt.amount <= 15,
                pt.price * 1.03,
                pt.price
            ) AS sale_price,

            rt.amount AS amount,

            rt.date_realization AS date_realization

        FROM dovidnyk_typiv_tovariv AS dtt

        INNER JOIN preyskurant_tovariv AS pt
            ON pt.id_type_tovar = dtt.id

        INNER JOIN dovidnyk_firmu_vyrobnyka AS dfv
            ON dfv.id = pt.id_firm

        INNER JOIN realizatsia_tovariv AS rt
            ON rt.id_preyskurant = pt.id

        ORDER BY rt.amount DESC

        LIMIT :limit_value
    """)

    result = await db.execute(
        sql,
        {
            "limit_value": 5
        }
    )

    return templates.TemplateResponse(
        "lab4_query3.html",
        {
            "request": request,
            "rows": result.mappings().all()
        }
    )


@router.get(path="/p1/", response_class=HTMLResponse)
async def p1_page(request: Request):
    return templates.TemplateResponse(
        "p1.html",
        {
            "request": request,
            "rows": None
        }
    )


@router.post(path="/p1/", response_class=HTMLResponse)
async def p1_execute(
    request: Request,
    start_date: str = Form(...),
    end_date: str = Form(...),
    db: AsyncSession = Depends(get_db)
):

    sql = text("CALL p1(:start_date, :end_date)")

    result = await db.execute(
        sql,
        {
            "start_date": start_date,
            "end_date": end_date
        }
    )

    return templates.TemplateResponse(
        "p1.html",
        {
            "request": request,
            "rows": result.mappings().all()
        }
    )


@router.get(path="/p2/", response_class=HTMLResponse)
async def p2(
    request: Request,
    db: AsyncSession = Depends(get_db)
):

    sql = text("CALL p2()")

    result = await db.execute(sql)

    return templates.TemplateResponse(
        "p2.html",
        {
            "request": request,
            "rows": result.mappings().all()
        }
    )


@router.get(path="/p3/", response_class=HTMLResponse)
async def p3_page(request: Request):

    return templates.TemplateResponse(
        "p3.html",
        {
            "request": request,
            "rows": None
        }
    )


@router.post(path="/p3/", response_class=HTMLResponse)
async def p3_execute(
    request: Request,
    num_days: int = Form(...),
    db: AsyncSession = Depends(get_db)
):

    sql = text("CALL p3(:num_days)")

    result = await db.execute(
        sql,
        {
            "num_days": num_days
        }
    )

    return templates.TemplateResponse(
        "p3.html",
        {
            "request": request,
            "rows": result.mappings().all()
        }
    )


@router.get(path="/p4/", response_class=HTMLResponse)
async def p4_page(request: Request):

    return templates.TemplateResponse(
        "p4.html",
        {
            "request": request,
            "rows": None
        }
    )


@router.post(path="/p4/", response_class=HTMLResponse)
async def p4_execute(
    request: Request,
    firm_name: str = Form(default=""),
    db: AsyncSession = Depends(get_db)
):

    sql = text("CALL p4(:firm_name)")

    result = await db.execute(
        sql,
        {
            "firm_name": firm_name
        }
    )

    return templates.TemplateResponse(
        "p4.html",
        {
            "request": request,
            "rows": result.mappings().all()
        }
    )


@router.get(path="/p5/", response_class=HTMLResponse)
async def p5_page(request: Request):
    return templates.TemplateResponse(
        "p5.html",
        {
            "request": request,
            "rows": None
        }
    )


@router.post(path="/p5/", response_class=HTMLResponse)
async def p5_execute(
    request: Request,
    target_year: int = Form(default=None),
    target_month: int = Form(default=None),
    db: AsyncSession = Depends(get_db)
):

    sql = text("""
        CALL p5(
            :target_year,
            :target_month
        )
    """)

    result = await db.execute(
        sql,
        {
            "target_year": target_year,
            "target_month": target_month
        }
    )

    return templates.TemplateResponse(
        "p5.html",
        {
            "request": request,
            "rows": result.mappings().all()
        }
    )
