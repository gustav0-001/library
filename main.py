from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers.books import router as books_router
from database import engine, Model


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

        print("БД инициализирована")

        yield

        print("БД: close")

        await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(books_router)
