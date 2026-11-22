from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlmodel import Session

from app.producto_categoria.model import ProductoCategoria

from . import repository
from .model import Categoria
from .schema import CategoriaCreate, CategoriaUpdate


def _normalizar_nombre(nombre: str) -> str:
    return nombre.strip().lower()


def _validar_nombre_unico(
    session: Session,
    nombre: str,
    excluir_id: int | None = None,
) -> None:
    existente = repository.obtener_por_nombre_normalizado(
        session,
        _normalizar_nombre(nombre),
        excluir_id=excluir_id,
    )
    if existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una categoría con ese nombre",
        )


def listar_categorias(session: Session) -> list[Categoria]:
    return repository.listar(session)


def obtener_categoria(session: Session, categoria_id: int) -> Categoria:
    categoria = repository.obtener_por_id(session, categoria_id)
    if categoria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )
    return categoria


def crear_categoria(session: Session, data: CategoriaCreate) -> Categoria:
    _validar_nombre_unico(session, data.nombre)
    categoria = Categoria(**data.model_dump())
    repository.agregar(session, categoria)
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

    repository.agregar(session, categoria)
    try:
        session.commit()
        session.refresh(categoria)
    except Exception:
        session.rollback()
        raise
    return categoria


def eliminar_categoria(session: Session, categoria_id: int) -> None:
    categoria = obtener_categoria(session, categoria_id)
    # Elimina primero vínculos para mantener integridad referencial.
    session.execute(
        delete(ProductoCategoria).where(
            ProductoCategoria.categoria_id == categoria_id
        )
    )
    repository.eliminar(session, categoria)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
