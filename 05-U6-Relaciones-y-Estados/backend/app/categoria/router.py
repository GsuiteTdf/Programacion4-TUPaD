from fastapi import APIRouter, Path, Response, status

from app.core.database import SessionDep

from . import service
from .schema import CategoriaCreate, CategoriaPublic, CategoriaUpdate


router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get(
    "/",
    response_model=list[CategoriaPublic],
    status_code=status.HTTP_200_OK,
    summary="Listar categorías",
)
def listar_categorias(session: SessionDep) -> list[CategoriaPublic]:
    return service.listar_categorias(session)


@router.get(
    "/{categoria_id}",
    response_model=CategoriaPublic,
    status_code=status.HTTP_200_OK,
    summary="Consultar una categoría",
)
def obtener_categoria(
    session: SessionDep,
    categoria_id: int = Path(..., gt=0),
) -> CategoriaPublic:
    return service.obtener_categoria(session, categoria_id)


@router.post(
    "/",
    response_model=CategoriaPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una categoría",
)
def crear_categoria(data: CategoriaCreate, session: SessionDep) -> CategoriaPublic:
    return service.crear_categoria(session, data)


@router.put(
    "/{categoria_id}",
    response_model=CategoriaPublic,
    status_code=status.HTTP_200_OK,
    summary="Editar una categoría",
)
def actualizar_categoria(
    data: CategoriaUpdate,
    session: SessionDep,
    categoria_id: int = Path(..., gt=0),
) -> CategoriaPublic:
    return service.actualizar_categoria(session, categoria_id, data)


@router.delete(
    "/{categoria_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una categoría",
)
def eliminar_categoria(
    session: SessionDep,
    categoria_id: int = Path(..., gt=0),
) -> Response:
    service.eliminar_categoria(session, categoria_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
