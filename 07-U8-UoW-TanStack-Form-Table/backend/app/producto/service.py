from fastapi import HTTPException

from .model import Producto, ProductoCategoria
from .schema import (
    ProductoCategoriaCreate,
    ProductoCategoriaPublic,
    ProductoCreate,
    ProductoPublic,
    ProductoUpdate,
)
from .unit_of_work import ProductoUnitOfWork


def _public(producto: Producto) -> ProductoPublic:
    return ProductoPublic.model_validate(producto)


def listar_productos() -> list[ProductoPublic]:
    with ProductoUnitOfWork() as uow:
        return [_public(item) for item in uow.productos.list_ordered()]


def obtener_producto(producto_id: int) -> ProductoPublic:
    with ProductoUnitOfWork() as uow:
        producto = uow.productos.get_by_id(producto_id)
        if producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return _public(producto)


def crear_producto(data: ProductoCreate) -> ProductoPublic:
    with ProductoUnitOfWork() as uow:
        producto = uow.productos.create(Producto(**data.model_dump()))
        return _public(producto)


def actualizar_producto(producto_id: int, data: ProductoUpdate) -> ProductoPublic:
    with ProductoUnitOfWork() as uow:
        producto = uow.productos.get_by_id(producto_id)
        if producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        for campo, valor in data.model_dump().items():
            setattr(producto, campo, valor)
        uow.session.add(producto)
        uow.session.flush()
        return _public(producto)


def eliminar_producto(producto_id: int) -> None:
    with ProductoUnitOfWork() as uow:
        producto = uow.productos.get_by_id(producto_id)
        if producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        # UML: DetallePedido.producto_id es FK con RESTRICT. Sin esta validación,
        # PostgreSQL rechaza el DELETE y el cliente recibe un error 500.
        if uow.productos.has_pedidos(producto_id):
            raise HTTPException(
                status_code=409,
                detail="No se puede eliminar un producto incluido en pedidos",
            )
        uow.relaciones.delete_by_producto(producto_id)
        uow.productos.delete(producto)


def asignar_categoria(
    producto_id: int,
    data: ProductoCategoriaCreate,
) -> ProductoCategoriaPublic:
    with ProductoUnitOfWork() as uow:
        if uow.productos.get_by_id(producto_id) is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        if uow.categorias.get_by_id(data.categoria_id) is None:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        if uow.relaciones.get_link(producto_id, data.categoria_id) is not None:
            raise HTTPException(status_code=409, detail="El producto ya está asociado a esa categoría")
        if data.es_principal:
            uow.relaciones.unset_principal(producto_id)
        link = uow.relaciones.create(
            ProductoCategoria(
                producto_id=producto_id,
                categoria_id=data.categoria_id,
                es_principal=data.es_principal,
            )
        )
        return ProductoCategoriaPublic.model_validate(link)


def listar_categorias_producto(producto_id: int) -> list[ProductoCategoriaPublic]:
    with ProductoUnitOfWork() as uow:
        if uow.productos.get_by_id(producto_id) is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return [
            ProductoCategoriaPublic.model_validate(link)
            for link in uow.relaciones.list_by_producto(producto_id)
        ]


def quitar_categoria(producto_id: int, categoria_id: int) -> None:
    with ProductoUnitOfWork() as uow:
        if uow.productos.get_by_id(producto_id) is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        link = uow.relaciones.get_link(producto_id, categoria_id)
        if link is None:
            raise HTTPException(status_code=404, detail="Asociación no encontrada")
        uow.relaciones.delete(link)
