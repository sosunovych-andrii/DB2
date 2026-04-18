from fastapi import APIRouter, Request, Form, Depends
from passlib.context import CryptContext
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse, RedirectResponse

from src.database.models.user import User
from src.database.settings import get_db
from src.templates_config import templates

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


@router.get(path="/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post(path="/register")
async def register(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    url: str | None = Form(None),
    phone: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.email == email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        return HTMLResponse("""
            <h2 style="color:red;">Email вже існує ❌</h2>
            <a href="/register">Назад</a>
        """)

    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        url=url,
        phone=phone
    )

    db.add(user)
    await db.execute(text(f"""
        CREATE USER '{name}'@'%' IDENTIFIED BY '{password}'
    """))
    await db.execute(text(f"""
        GRANT SELECT, INSERT, UPDATE
        ON *.*
        TO '{name}'@'%'
    """))
    await db.commit()

    return HTMLResponse("""
        <h2 style="color:green;">Користувача створено ✅</h2>
        <a href="/login">Перейти до логіну</a>
    """)


@router.get(path="/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post(path="/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        return HTMLResponse("""
            <h2 style="color:red;">Невірні дані ❌</h2>
            <a href="/login">Спробувати ще раз</a>
        """)

    return HTMLResponse("""
        <h2 style="color:green;">Вхід виконано успішно ✅</h2>
        <a href="/">На головну</a>
    """)
