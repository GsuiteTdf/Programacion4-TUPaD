from fastapi import HTTPException

from .model import Ingrediente
from .schema import IngredienteCreate, IngredientePublic, IngredienteUpdate
from .unit_of_work import IngredienteUnitOfWork


def _public(item: Ingrediente) -> IngredientePublic:
    return IngredientePublic.model_validate(item)


def listar_ingredientes() -> list[IngredientePublic]:
    with IngredienteUnitOfWork() as uow:
        return [_public(item) for item in uow.ingredientes.list_ordered()]


def obtener_ingrediente(ingrediente_id: int) -> IngredientePublic:
    with IngredienteUnitOfWork() as uow:
        item = uow.ingredientes.get_by_id(ingrediente_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
        return _public(item)


def crear_ingrediente(data: IngredienteCreate) -> IngredientePublic:
    with IngredienteUnitOfWork() as uow:
        item = uow.ingredientes.create(Ingrediente(**data.model_dump()))
        return _public(item)


def actualizar_ingrediente(ingrediente_id: int, data: IngredienteUpdate) -> IngredientePublic:
    with IngredienteUnitOfWork() as uow:
        item = uow.ingredientes.get_by_id(ingrediente_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
        item.nombre = data.nombre
        uow.session.add(item)
        uow.session.flush()
        return _public(item)


def eliminar_ingrediente(ingrediente_id: int) -> None:
    with IngredienteUnitOfWork() as uow:
        item = uow.ingredientes.get_by_id(ingrediente_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
        uow.ingredientes.delete(item)
