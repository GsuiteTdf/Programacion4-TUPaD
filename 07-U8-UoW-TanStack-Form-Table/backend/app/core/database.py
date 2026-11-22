import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/foodstore_u8",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def create_db_and_tables() -> None:
    # Importar modelos registra todas las tablas en SQLModel.metadata.
    from app.categoria.model import Categoria  # noqa: F401
    from app.ingrediente.model import Ingrediente  # noqa: F401
    from app.pedido.model import DetallePedido, Pedido  # noqa: F401
    from app.producto.model import Producto, ProductoCategoria  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
