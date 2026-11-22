from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.categoria.router import router as categoria_router
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.ingrediente.router import router as ingrediente_router
from app.modules.catalogos.router import router as catalogos_router
from app.modules.usuarios.router import router as auth_router
from app.pedido.router import router as pedido_router
from app.producto.router import router as producto_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Food Store - Unidad 9 (+ ingredientes para la Unidad 10)",
    description="JWT HttpOnly + RBAC + Zustand/Axios",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(catalogos_router)
app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(ingrediente_router)
app.include_router(pedido_router)


@app.get("/", tags=["sistema"])
def inicio() -> dict[str, str]:
    return {"mensaje": "Food Store API - Unidad 9"}
