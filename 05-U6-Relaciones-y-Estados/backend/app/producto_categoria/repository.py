from sqlmodel import Session, select

from .model import ProductoCategoria


def listar(session: Session) -> list[ProductoCategoria]:
    statement = select(ProductoCategoria).order_by(
        ProductoCategoria.producto_id,
        ProductoCategoria.categoria_id,
    )
    return list(session.exec(statement).all())


def obtener(
    session: Session,
    producto_id: int,
    categoria_id: int,
) -> ProductoCategoria | None:
    return session.get(ProductoCategoria, (producto_id, categoria_id))


def agregar(session: Session, relacion: ProductoCategoria) -> None:
    session.add(relacion)


def eliminar(session: Session, relacion: ProductoCategoria) -> None:
    session.delete(relacion)
