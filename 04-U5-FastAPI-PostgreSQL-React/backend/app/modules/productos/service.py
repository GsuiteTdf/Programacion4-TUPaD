from fastapi import HTTPException, status
from sqlmodel import Session

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


def listar_productos(
    session: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Producto]:
    return repository.listar(session, skip=skip, limit=limit)


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

    try:
        repository.agregar(session, producto)
        session.commit()
        session.refresh(producto)
        return producto
    except Exception:
        session.rollback()
        raise


def actualizar_producto(
    session: Session,
    producto_id: int,
    data: ProductoUpdate,
) -> Producto:
    producto = obtener_producto(session, producto_id)
    _validar_nombre_unico(session, data.nombre, excluir_id=producto_id)
    producto.sqlmodel_update(data.model_dump())

    try:
        repository.agregar(session, producto)
        session.commit()
        session.refresh(producto)
        return producto
    except Exception:
        session.rollback()
        raise


def eliminar_producto(session: Session, producto_id: int) -> None:
    producto = obtener_producto(session, producto_id)

    try:
        repository.eliminar(session, producto)
        session.commit()
    except Exception:
        session.rollback()
        raise
