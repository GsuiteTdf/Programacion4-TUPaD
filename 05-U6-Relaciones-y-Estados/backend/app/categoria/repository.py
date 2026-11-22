from sqlmodel import Session, func, select

from .model import Categoria


def listar(session: Session) -> list[Categoria]:
    statement = select(Categoria).order_by(Categoria.id)
    return list(session.exec(statement).all())


def obtener_por_id(session: Session, categoria_id: int) -> Categoria | None:
    return session.get(Categoria, categoria_id)


def obtener_por_nombre_normalizado(
    session: Session,
    nombre_normalizado: str,
    excluir_id: int | None = None,
) -> Categoria | None:
    statement = select(Categoria).where(
        func.lower(func.trim(Categoria.nombre)) == nombre_normalizado
    )
    if excluir_id is not None:
        statement = statement.where(Categoria.id != excluir_id)
    return session.exec(statement).first()


def agregar(session: Session, categoria: Categoria) -> None:
    session.add(categoria)


def eliminar(session: Session, categoria: Categoria) -> None:
    session.delete(categoria)
