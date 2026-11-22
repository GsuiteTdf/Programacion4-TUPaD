from fastapi import APIRouter, Response, status

from .schema import IngredienteCreate, IngredientePublic, IngredienteUpdate
from .service import (
    actualizar_ingrediente,
    crear_ingrediente,
    eliminar_ingrediente,
    listar_ingredientes,
    obtener_ingrediente,
)

router = APIRouter(prefix="/ingredientes", tags=["ingredientes"])


@router.get("", response_model=list[IngredientePublic])
def listar() -> list[IngredientePublic]:
    return listar_ingredientes()


@router.get("/{ingrediente_id}", response_model=IngredientePublic)
def obtener(ingrediente_id: int) -> IngredientePublic:
    return obtener_ingrediente(ingrediente_id)


@router.post("", response_model=IngredientePublic, status_code=status.HTTP_201_CREATED)
def crear(data: IngredienteCreate) -> IngredientePublic:
    return crear_ingrediente(data)


@router.put("/{ingrediente_id}", response_model=IngredientePublic)
def actualizar(ingrediente_id: int, data: IngredienteUpdate) -> IngredientePublic:
    return actualizar_ingrediente(ingrediente_id, data)


@router.delete("/{ingrediente_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def eliminar(ingrediente_id: int) -> Response:
    eliminar_ingrediente(ingrediente_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
