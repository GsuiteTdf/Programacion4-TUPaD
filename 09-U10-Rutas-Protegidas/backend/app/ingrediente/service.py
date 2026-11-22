from datetime import datetime, timezone

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
        if uow.ingredientes.find_by_normalized_name(data.nombre) is not None:
            raise HTTPException(status_code=409, detail="Ya existe un ingrediente con ese nombre")
        return _public(uow.ingredientes.create(Ingrediente(nombre=data.nombre)))


def actualizar_ingrediente(ingrediente_id: int, data: IngredienteUpdate) -> IngredientePublic:
    with IngredienteUnitOfWork() as uow:
        item = uow.ingredientes.get_by_id(ingrediente_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
        repetido = uow.ingredientes.find_by_normalized_name(data.nombre)
        if repetido is not None and repetido.id != ingrediente_id:
            raise HTTPException(status_code=409, detail="Ya existe un ingrediente con ese nombre")
        item.nombre = data.nombre
        item.updated_at = datetime.now(timezone.utc)
        uow.session.add(item)
        uow.session.flush()
        return _public(item)


def eliminar_ingrediente(ingrediente_id: int) -> None:
    with IngredienteUnitOfWork() as uow:
        item = uow.ingredientes.get_by_id(ingrediente_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
        # Borrado lógico, igual que Categoria y Producto.
        now = datetime.now(timezone.utc)
        item.deleted_at = now
        item.updated_at = now
        uow.session.add(item)
        uow.session.flush()
