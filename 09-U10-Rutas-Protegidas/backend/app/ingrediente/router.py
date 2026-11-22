from fastapi import APIRouter, Depends, Response, status

from app.core.security import get_current_active_user, require_role

from .schema import IngredienteCreate, IngredientePublic, IngredienteUpdate
from .service import (
    actualizar_ingrediente,
    crear_ingrediente,
    eliminar_ingrediente,
    listar_ingredientes,
    obtener_ingrediente,
)

# Mismas reglas que categorías: lectura para cualquier usuario autenticado,
# escritura solo para admin.
router = APIRouter(prefix="/ingredientes", tags=["ingredientes"])


@router.get("", response_model=list[IngredientePublic], dependencies=[Depends(get_current_active_user)])
def listar() -> list[IngredientePublic]:
    return listar_ingredientes()


@router.get("/{ingrediente_id}", response_model=IngredientePublic, dependencies=[Depends(get_current_active_user)])
def obtener(ingrediente_id: int) -> IngredientePublic:
    return obtener_ingrediente(ingrediente_id)


@router.post("", response_model=IngredientePublic, status_code=201, dependencies=[Depends(require_role(["admin"]))])
def crear(data: IngredienteCreate) -> IngredientePublic:
    return crear_ingrediente(data)


@router.put("/{ingrediente_id}", response_model=IngredientePublic, dependencies=[Depends(require_role(["admin"]))])
def actualizar(ingrediente_id: int, data: IngredienteUpdate) -> IngredientePublic:
    return actualizar_ingrediente(ingrediente_id, data)


@router.delete("/{ingrediente_id}", status_code=204, response_model=None, dependencies=[Depends(require_role(["admin"]))])
def eliminar(ingrediente_id: int) -> Response:
    eliminar_ingrediente(ingrediente_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
