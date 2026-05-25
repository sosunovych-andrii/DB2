from fastapi import FastAPI

from src.routers.tables import router as tables_router
from src.routers.sales import router as sales_router
from src.routers.manufacturers import router as manufacturers_router
from src.routers.price_list import router as price_list_router
from src.routers.product_types import router as product_types_router
from src.routers.auth import router as users_router
from src.routers.mk1 import router as mk1_router
from src.routers.lab4 import router as lab4_router
from src.routers.lab5 import router as lab5_router
from src.routers.mk2 import router as mk2_router


app = FastAPI()


app.include_router(router=tables_router)
app.include_router(router=sales_router)
app.include_router(router=manufacturers_router)
app.include_router(router=price_list_router)
app.include_router(router=product_types_router)
app.include_router(router=users_router)
app.include_router(router=mk1_router)
app.include_router(router=lab4_router)
app.include_router(router=lab5_router)
app.include_router(router=mk2_router)