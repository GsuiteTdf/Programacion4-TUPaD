from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.categoria.router import router as categoria_router
from app.core.database import create_db_and_tables
from app.producto.router import router as producto_router
from app.producto_categoria.router import router as producto_categoria_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Food Store - Unidad 6",
    description="CRUD Categorías + CRUD Productos + relación ProductoCategoria",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(producto_categoria_router)


@app.get("/", tags=["Sistema"])
def inicio() -> dict[str, str]:
    return {"mensaje": "Food Store API - Unidad 6"}
