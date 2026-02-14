from fastapi import FastAPI

from src.routers.tables import router

app = FastAPI()

app.include_router(router=router)
