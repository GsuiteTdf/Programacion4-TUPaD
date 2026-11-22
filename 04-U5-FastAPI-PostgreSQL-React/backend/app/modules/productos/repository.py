from sqlmodel import Session, func, select

from .model import Producto


def listar(session: Session, skip: int = 0, limit: int = 100) -> list[Producto]:
    statement = select(Producto).order_by(Producto.id).offset(skip).limit(limit)
    return list(session.exec(statement).all())


def obtener_por_id(session: Session, producto_id: int) -> Producto | None:
    return session.get(Producto, producto_id)


def obtener_por_nombre_normalizado(
    session: Session,
    nombre_normalizado: str,
    excluir_id: int | None = None,
) -> Producto | None:
    statement = select(Producto).where(
        func.lower(func.trim(Producto.nombre)) == nombre_normalizado
    )
    if excluir_id is not None:
        statement = statement.where(Producto.id != excluir_id)
    return session.exec(statement).first()


def agregar(session: Session, producto: Producto) -> None:
    session.add(producto)


def eliminar(session: Session, producto: Producto) -> None:
    session.delete(producto)
