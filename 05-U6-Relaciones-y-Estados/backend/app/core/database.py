import os
from collections.abc import Generator
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine


load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/foodstore",
)

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)


def create_db_and_tables() -> None:
    """Crea las tablas del TP si todavía no existen."""
    # Importar modelos registra todas las tablas en SQLModel.metadata.
    from app.categoria.model import Categoria  # noqa: F401
    from app.producto.model import Producto  # noqa: F401
    from app.producto_categoria.model import ProductoCategoria  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Entrega una sesión de base de datos por request."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
