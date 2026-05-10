from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession
)

from sqlalchemy.orm import sessionmaker


URL_DATABASE = (
    "mysql+aiomysql://root:1111@localhost:3306/lab1"
)

engine = create_async_engine(
    URL_DATABASE
)

AsyncSessionLocal = sessionmaker( #type: ignore
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
