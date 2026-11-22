from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.categoria.model import Categoria

from .model import Producto, ProductoCategoria
from .schema import ProductoCreate, ProductoUpdate


def listar_productos(session: Session) -> list[Producto]:
    statement = select(Producto).order_by(Producto.id)
    return list(session.exec(statement).all())


def obtener_producto(session: Session, producto_id: int) -> Producto:
    producto = session.get(Producto, producto_id)
    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )
    return producto


def crear_producto(session: Session, data: ProductoCreate) -> Producto:
    producto = Producto(**data.model_dump())
    session.add(producto)
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
    for campo, valor in data.model_dump().items():
        setattr(producto, campo, valor)

    session.add(producto)
    try:
        session.commit()
        session.refresh(producto)
    except Exception:
        session.rollback()
        raise
    return producto


def eliminar_producto(session: Session, producto_id: int) -> None:
    producto = obtener_producto(session, producto_id)

    relaciones = session.exec(
        select(ProductoCategoria).where(
            ProductoCategoria.producto_id == producto_id
        )
    ).all()
    for relacion in relaciones:
        session.delete(relacion)
    # Sin Relationship, SQLAlchemy no conoce el orden de borrado: se envían primero
    # los DELETE de la tabla de enlace para no violar la clave foránea.
    session.flush()

    session.delete(producto)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise


def asignar_categoria(
    session: Session,
    producto_id: int,
    categoria_id: int,
) -> ProductoCategoria:
    obtener_producto(session, producto_id)
    categoria = session.get(Categoria, categoria_id)
    if categoria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )

    existente = session.get(
        ProductoCategoria,
        (producto_id, categoria_id),
    )
    if existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El producto ya está asociado a esa categoría",
        )

    relacion = ProductoCategoria(
        producto_id=producto_id,
        categoria_id=categoria_id,
    )
    session.add(relacion)
    try:
        session.commit()
        session.refresh(relacion)
    except Exception:
        session.rollback()
        raise
    return relacion


def listar_categorias_producto(
    session: Session,
    producto_id: int,
) -> list[Categoria]:
    obtener_producto(session, producto_id)
    statement = (
        select(Categoria)
        .join(
            ProductoCategoria,
            Categoria.id == ProductoCategoria.categoria_id,
        )
        .where(ProductoCategoria.producto_id == producto_id)
        .order_by(Categoria.id)
    )
    return list(session.exec(statement).all())


def quitar_categoria(
    session: Session,
    producto_id: int,
    categoria_id: int,
) -> None:
    obtener_producto(session, producto_id)
    relacion = session.get(
        ProductoCategoria,
        (producto_id, categoria_id),
    )
    if relacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asociación producto-categoría no encontrada",
        )

    session.delete(relacion)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
