from fastapi import HTTPException, status
from sqlmodel import Session, func, select

from app.producto.model import ProductoCategoria

from .model import Categoria
from .schema import CategoriaCreate, CategoriaUpdate


def _validar_nombre_unico(
    session: Session,
    nombre: str,
    excluir_id: int | None = None,
) -> None:
    """UML: Categoria.nombre es único. Se compara sin mayúsculas ni espacios extremos."""
    statement = select(Categoria).where(
        func.lower(func.trim(Categoria.nombre)) == nombre.strip().lower()
    )
    if excluir_id is not None:
        statement = statement.where(Categoria.id != excluir_id)
    if session.exec(statement).first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una categoría con ese nombre",
        )


def listar_categorias(session: Session) -> list[Categoria]:
    statement = select(Categoria).order_by(Categoria.id)
    return list(session.exec(statement).all())


def obtener_categoria(session: Session, categoria_id: int) -> Categoria:
    categoria = session.get(Categoria, categoria_id)
    if categoria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )
    return categoria


def crear_categoria(session: Session, data: CategoriaCreate) -> Categoria:
    _validar_nombre_unico(session, data.nombre)
    categoria = Categoria(**data.model_dump())
    session.add(categoria)
    try:
        session.commit()
        session.refresh(categoria)
    except Exception:
        session.rollback()
        raise
    return categoria


def actualizar_categoria(
    session: Session,
    categoria_id: int,
    data: CategoriaUpdate,
) -> Categoria:
    categoria = obtener_categoria(session, categoria_id)
    _validar_nombre_unico(session, data.nombre, excluir_id=categoria_id)
    for campo, valor in data.model_dump().items():
        setattr(categoria, campo, valor)

    session.add(categoria)
    try:
        session.commit()
        session.refresh(categoria)
    except Exception:
        session.rollback()
        raise
    return categoria


def eliminar_categoria(session: Session, categoria_id: int) -> None:
    categoria = obtener_categoria(session, categoria_id)

    relaciones = session.exec(
        select(ProductoCategoria).where(
            ProductoCategoria.categoria_id == categoria_id
        )
    ).all()
    for relacion in relaciones:
        session.delete(relacion)
    # Sin Relationship, SQLAlchemy no conoce el orden de borrado: se envían primero
    # los DELETE de la tabla de enlace para no violar la clave foránea.
    session.flush()

    session.delete(categoria)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
