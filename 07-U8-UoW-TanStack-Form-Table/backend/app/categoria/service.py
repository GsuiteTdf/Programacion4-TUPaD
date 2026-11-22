from fastapi import HTTPException, status

from .model import Categoria
from .schema import CategoriaCreate, CategoriaPublic, CategoriaUpdate
from .unit_of_work import CategoriaUnitOfWork


def _public(categoria: Categoria) -> CategoriaPublic:
    return CategoriaPublic.model_validate(categoria)


def listar_categorias() -> list[CategoriaPublic]:
    with CategoriaUnitOfWork() as uow:
        return [_public(item) for item in uow.categorias.list_ordered()]


def obtener_categoria(categoria_id: int) -> CategoriaPublic:
    with CategoriaUnitOfWork() as uow:
        categoria = uow.categorias.get_by_id(categoria_id)
        if categoria is None:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return _public(categoria)


def crear_categoria(data: CategoriaCreate) -> CategoriaPublic:
    with CategoriaUnitOfWork() as uow:
        if uow.categorias.find_by_normalized_name(data.nombre) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una categoría con ese nombre",
            )
        categoria = uow.categorias.create(Categoria(**data.model_dump()))
        return _public(categoria)


def actualizar_categoria(categoria_id: int, data: CategoriaUpdate) -> CategoriaPublic:
    with CategoriaUnitOfWork() as uow:
        categoria = uow.categorias.get_by_id(categoria_id)
        if categoria is None:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        repetida = uow.categorias.find_by_normalized_name(data.nombre)
        if repetida is not None and repetida.id != categoria_id:
            raise HTTPException(status_code=409, detail="Ya existe una categoría con ese nombre")
        categoria.nombre = data.nombre
        categoria.descripcion = data.descripcion
        uow.session.add(categoria)
        uow.session.flush()
        return _public(categoria)


def eliminar_categoria(categoria_id: int) -> None:
    with CategoriaUnitOfWork() as uow:
        categoria = uow.categorias.get_by_id(categoria_id)
        if categoria is None:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        # RN-05 es opcional en la guía; se implementa para preservar integridad.
        if uow.categorias.has_products(categoria_id):
            raise HTTPException(
                status_code=409,
                detail="No se puede eliminar una categoría con productos asociados",
            )
        uow.categorias.delete(categoria)
