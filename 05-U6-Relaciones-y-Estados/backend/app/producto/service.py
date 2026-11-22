from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlmodel import Session

from app.producto_categoria.model import ProductoCategoria

from . import repository
from .model import Producto
from .schema import ProductoCreate, ProductoUpdate


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
            detail="Ya existe un producto con ese nombre",
        )


def listar_productos(session: Session) -> list[Producto]:
    return repository.listar(session)


def obtener_producto(session: Session, producto_id: int) -> Producto:
    producto = repository.obtener_por_id(session, producto_id)
    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )
    return producto


def crear_producto(session: Session, data: ProductoCreate) -> Producto:
    _validar_nombre_unico(session, data.nombre)
    producto = Producto(**data.model_dump())
    repository.agregar(session, producto)
    try:
        session.commit()
        session.refresh(producto)
    except Exception:
        session.rollback()
        raise
    return producto


def actualizar_producto(
    session: Session,
    producto_id: int,
    data: ProductoUpdate,
) -> Producto:
    producto = obtener_producto(session, producto_id)
    _validar_nombre_unico(session, data.nombre, excluir_id=producto_id)

    for campo, valor in data.model_dump().items():
        setattr(producto, campo, valor)

    repository.agregar(session, producto)
    try:
        session.commit()
        session.refresh(producto)
    except Exception:
        session.rollback()
        raise
    return producto


def eliminar_producto(session: Session, producto_id: int) -> None:
    producto = obtener_producto(session, producto_id)
    session.execute(
        delete(ProductoCategoria).where(
            ProductoCategoria.producto_id == producto_id
        )
    )
    repository.eliminar(session, producto)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
