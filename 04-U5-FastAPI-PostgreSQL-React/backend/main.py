from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import create_db_and_tables
from app.modules.productos import model  # noqa: F401 - registra metadata SQLModel
from app.modules.productos.router import router as productos_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Food Store - Gestor de Productos",
    version="1.0.0",
    description="TPI Unidad 5 - FastAPI, SQLModel y PostgreSQL",
    lifespan=lifespan,
)

app.include_router(productos_router)


@app.get("/", tags=["Sistema"])
def healthcheck() -> dict[str, str]:
    return {"mensaje": "Food Store API operativa"}
