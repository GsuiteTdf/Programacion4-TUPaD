from fastapi import APIRouter, Path, Response, status

from app.categoria.schema import CategoriaPublic
from app.core.database import SessionDep

from . import service
from .schema import (
    ProductoCategoriaCreate,
    ProductoCategoriaPublic,
    ProductoCreate,
    ProductoPublic,
    ProductoUpdate,
)

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get(
    "/",
    response_model=list[ProductoPublic],
    status_code=status.HTTP_200_OK,
    summary="Listar productos",
)
def listar_productos(session: SessionDep) -> list[ProductoPublic]:
    return service.listar_productos(session)


@router.get(
    "/{producto_id}",
    response_model=ProductoPublic,
    status_code=status.HTTP_200_OK,
    summary="Consultar producto",
)
def obtener_producto(
    session: SessionDep,
    producto_id: int = Path(..., gt=0),
) -> ProductoPublic:
    return service.obtener_producto(session, producto_id)


@router.post(
    "/",
    response_model=ProductoPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Crear producto",
)
def crear_producto(
    data: ProductoCreate,
    session: SessionDep,
) -> ProductoPublic:
    return service.crear_producto(session, data)


@router.put(
    "/{producto_id}",
    response_model=ProductoPublic,
    status_code=status.HTTP_200_OK,
    summary="Editar producto",
)
def actualizar_producto(
    data: ProductoUpdate,
    session: SessionDep,
    producto_id: int = Path(..., gt=0),
) -> ProductoPublic:
    return service.actualizar_producto(session, producto_id, data)


@router.delete(
    "/{producto_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar producto",
)
def eliminar_producto(
    session: SessionDep,
    producto_id: int = Path(..., gt=0),
) -> Response:
    service.eliminar_producto(session, producto_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{producto_id}/categorias",
    response_model=ProductoCategoriaPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Asignar categoría a un producto",
)
def asignar_categoria(
    data: ProductoCategoriaCreate,
    session: SessionDep,
    producto_id: int = Path(..., gt=0),
) -> ProductoCategoriaPublic:
    return service.asignar_categoria(
        session,
        producto_id,
        data.categoria_id,
    )


@router.get(
    "/{producto_id}/categorias",
    response_model=list[CategoriaPublic],
    status_code=status.HTTP_200_OK,
    summary="Listar categorías de un producto",
)
def listar_categorias_producto(
    session: SessionDep,
    producto_id: int = Path(..., gt=0),
) -> list[CategoriaPublic]:
    return service.listar_categorias_producto(session, producto_id)


@router.delete(
    "/{producto_id}/categorias/{categoria_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Quitar categoría de un producto",
)
def quitar_categoria(
    session: SessionDep,
    producto_id: int = Path(..., gt=0),
    categoria_id: int = Path(..., gt=0),
) -> Response:
    service.quitar_categoria(session, producto_id, categoria_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
