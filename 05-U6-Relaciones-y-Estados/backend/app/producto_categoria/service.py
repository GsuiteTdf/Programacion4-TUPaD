from fastapi import HTTPException, status
from sqlmodel import Session

from app.categoria.model import Categoria
from app.producto.model import Producto

from . import repository
from .model import ProductoCategoria
from .schema import ProductoCategoriaCreate, ProductoCategoriaUpdate


def _validar_referencias(
    session: Session,
    producto_id: int,
    categoria_id: int,
) -> None:
    if session.get(Producto, producto_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )
    if session.get(Categoria, categoria_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )


def listar_relaciones(session: Session) -> list[ProductoCategoria]:
    return repository.listar(session)


def obtener_relacion(
    session: Session,
    producto_id: int,
    categoria_id: int,
) -> ProductoCategoria:
    relacion = repository.obtener(session, producto_id, categoria_id)
    if relacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación ProductoCategoria no encontrada",
        )
    return relacion


def crear_relacion(
    session: Session,
    data: ProductoCategoriaCreate,
) -> ProductoCategoria:
    _validar_referencias(session, data.producto_id, data.categoria_id)
    if repository.obtener(session, data.producto_id, data.categoria_id) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La relación ProductoCategoria ya existe",
        )

    relacion = ProductoCategoria(**data.model_dump())
    repository.agregar(session, relacion)
    try:
        session.commit()
        session.refresh(relacion)
    except Exception:
        session.rollback()
        raise
    return relacion


def actualizar_relacion(
    session: Session,
    producto_id: int,
    categoria_id: int,
    data: ProductoCategoriaUpdate,
) -> ProductoCategoria:
    relacion = obtener_relacion(session, producto_id, categoria_id)
    _validar_referencias(session, data.producto_id, data.categoria_id)

    if (
        data.producto_id == producto_id
        and data.categoria_id == categoria_id
    ):
        return relacion

    destino = repository.obtener(session, data.producto_id, data.categoria_id)
    if destino is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La relación ProductoCategoria de destino ya existe",
        )

    repository.eliminar(session, relacion)
    session.flush()
    nueva_relacion = ProductoCategoria(**data.model_dump())
    repository.agregar(session, nueva_relacion)
    try:
        session.commit()
        session.refresh(nueva_relacion)
    except Exception:
        session.rollback()
        raise
    return nueva_relacion


def eliminar_relacion(
    session: Session,
    producto_id: int,
    categoria_id: int,
) -> None:
    relacion = obtener_relacion(session, producto_id, categoria_id)
    repository.eliminar(session, relacion)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
