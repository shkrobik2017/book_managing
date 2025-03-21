from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from src.routers.router import router
from src.db.db_setup import DB


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
    await DB.init_orm()

    yield

    await DB.close_orm()
app = FastAPI(lifespan=lifespan)

app.include_router(router=router)