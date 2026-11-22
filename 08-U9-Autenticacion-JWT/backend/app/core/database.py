from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)


def create_db_and_tables() -> None:
    # Los imports registran los modelos en SQLModel.metadata.
    from app.categoria.model import Categoria  # noqa: F401
    from app.modules.catalogos.model import EstadoPedido, FormaPago  # noqa: F401
    from app.modules.usuarios.model import Rol, Usuario, UsuarioRol  # noqa: F401
    from app.pedido.model import DetallePedido, Pedido  # noqa: F401
    from app.producto.model import Producto, ProductoCategoria  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
