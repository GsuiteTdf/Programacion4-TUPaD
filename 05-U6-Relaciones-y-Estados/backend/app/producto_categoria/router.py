from fastapi import APIRouter, Path, Response, status

from app.core.database import SessionDep

from . import service
from .schema import (
    ProductoCategoriaCreate,
    ProductoCategoriaPublic,
    ProductoCategoriaUpdate,
)


router = APIRouter(
    prefix="/producto-categorias",
    tags=["ProductoCategoria"],
)


@router.get(
    "/",
    response_model=list[ProductoCategoriaPublic],
    status_code=status.HTTP_200_OK,
    summary="Listar relaciones ProductoCategoria",
)
def listar_relaciones(session: SessionDep) -> list[ProductoCategoriaPublic]:
    return service.listar_relaciones(session)


@router.get(
    "/{producto_id}/{categoria_id}",
    response_model=ProductoCategoriaPublic,
    status_code=status.HTTP_200_OK,
    summary="Consultar una relación ProductoCategoria",
)
def obtener_relacion(
    session: SessionDep,
    producto_id: int = Path(..., gt=0),
    categoria_id: int = Path(..., gt=0),
) -> ProductoCategoriaPublic:
    return service.obtener_relacion(session, producto_id, categoria_id)


@router.post(
    "/",
    response_model=ProductoCategoriaPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una relación ProductoCategoria",
)
def crear_relacion(
    data: ProductoCategoriaCreate,
    session: SessionDep,
) -> ProductoCategoriaPublic:
    return service.crear_relacion(session, data)


@router.put(
    "/{producto_id}/{categoria_id}",
    response_model=ProductoCategoriaPublic,
    status_code=status.HTTP_200_OK,
    summary="Editar una relación ProductoCategoria",
)
def actualizar_relacion(
    data: ProductoCategoriaUpdate,
    session: SessionDep,
    producto_id: int = Path(..., gt=0),
    categoria_id: int = Path(..., gt=0),
) -> ProductoCategoriaPublic:
    return service.actualizar_relacion(
        session,
        producto_id,
        categoria_id,
        data,
    )


@router.delete(
    "/{producto_id}/{categoria_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una relación ProductoCategoria",
)
def eliminar_relacion(
    session: SessionDep,
    producto_id: int = Path(..., gt=0),
    categoria_id: int = Path(..., gt=0),
) -> Response:
    service.eliminar_relacion(session, producto_id, categoria_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
