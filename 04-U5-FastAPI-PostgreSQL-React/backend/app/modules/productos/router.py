from fastapi import APIRouter, Path, Query, Response, status

from app.core.database import SessionDep

from . import service
from .schema import ProductoCreate, ProductoPublic, ProductoUpdate


router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post(
    "/",
    response_model=ProductoPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un producto",
)
def crear_producto(data: ProductoCreate, session: SessionDep) -> ProductoPublic:
    return service.crear_producto(session, data)


@router.get(
    "/",
    response_model=list[ProductoPublic],
    status_code=status.HTTP_200_OK,
    summary="Listar productos",
)
def listar_productos(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
) -> list[ProductoPublic]:
    return service.listar_productos(session, skip=skip, limit=limit)


@router.get(
    "/{producto_id}",
    response_model=ProductoPublic,
    status_code=status.HTTP_200_OK,
    summary="Consultar un producto",
)
def obtener_producto(
    session: SessionDep,
    producto_id: int = Path(..., gt=0),
) -> ProductoPublic:
    return service.obtener_producto(session, producto_id)


@router.put(
    "/{producto_id}",
    response_model=ProductoPublic,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un producto",
)
def actualizar_producto(
    data: ProductoUpdate,
    session: SessionDep,
    producto_id: int = Path(..., gt=0),
) -> ProductoPublic:
    return service.actualizar_producto(session, producto_id, data)


@router.delete(
    "/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un producto",
)
def eliminar_producto(
    session: SessionDep,
    producto_id: int = Path(..., gt=0),
) -> Response:
    service.eliminar_producto(session, producto_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
