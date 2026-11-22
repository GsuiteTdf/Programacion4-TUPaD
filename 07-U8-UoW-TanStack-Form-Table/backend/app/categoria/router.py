from fastapi import APIRouter, Response, status

from .schema import CategoriaCreate, CategoriaPublic, CategoriaUpdate
from .service import (
    actualizar_categoria,
    crear_categoria,
    eliminar_categoria,
    listar_categorias,
    obtener_categoria,
)

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("/", response_model=list[CategoriaPublic])
def listar() -> list[CategoriaPublic]:
    return listar_categorias()


@router.get("/{categoria_id}", response_model=CategoriaPublic)
def obtener(categoria_id: int) -> CategoriaPublic:
    return obtener_categoria(categoria_id)


@router.post("/", response_model=CategoriaPublic, status_code=status.HTTP_201_CREATED)
def crear(data: CategoriaCreate) -> CategoriaPublic:
    return crear_categoria(data)


@router.put("/{categoria_id}", response_model=CategoriaPublic)
def actualizar(categoria_id: int, data: CategoriaUpdate) -> CategoriaPublic:
    return actualizar_categoria(categoria_id, data)


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def eliminar(categoria_id: int) -> Response:
    eliminar_categoria(categoria_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
