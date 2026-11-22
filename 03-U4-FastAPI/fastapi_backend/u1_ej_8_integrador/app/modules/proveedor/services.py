from fastapi import HTTPException, status

from .schemas import ProveedorCreate, ProveedorRead


db_proveedores: list[ProveedorRead] = []
id_counter = 1


def _codigo_en_uso(codigo: str, excluir_id: int | None = None) -> bool:
    return any(
        proveedor.codigo == codigo and proveedor.id != excluir_id
        for proveedor in db_proveedores
    )


def crear(data: ProveedorCreate) -> ProveedorRead:
    global id_counter

    if _codigo_en_uso(data.codigo):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un proveedor con ese código",
        )

    nuevo = ProveedorRead(id=id_counter, **data.model_dump())
    db_proveedores.append(nuevo)
    id_counter += 1
    return nuevo


def obtener_todos(
    skip: int = 0,
    limit: int = 10,
    activo: bool | None = None,
) -> list[ProveedorRead]:
    proveedores = db_proveedores
    if activo is not None:
        proveedores = [p for p in proveedores if p.activo is activo]
    return proveedores[skip : skip + limit]


def obtener_por_id(id: int) -> ProveedorRead:
    for proveedor in db_proveedores:
        if proveedor.id == id:
            return proveedor

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Proveedor no encontrado",
    )


def actualizar_total(id: int, data: ProveedorCreate) -> ProveedorRead:
    proveedor_actual = obtener_por_id(id)

    if _codigo_en_uso(data.codigo, excluir_id=id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un proveedor con ese código",
        )

    actualizado = ProveedorRead(id=proveedor_actual.id, **data.model_dump())
    for index, proveedor in enumerate(db_proveedores):
        if proveedor.id == id:
            db_proveedores[index] = actualizado
            return actualizado

    # La búsqueda inicial garantiza que este punto no debería alcanzarse.
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Proveedor no encontrado",
    )


def desactivar(id: int) -> ProveedorRead:
    proveedor = obtener_por_id(id)

    if not proveedor.activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El proveedor ya está desactivado",
        )

    actualizado = ProveedorRead(**{**proveedor.model_dump(), "activo": False})
    for index, actual in enumerate(db_proveedores):
        if actual.id == id:
            db_proveedores[index] = actualizado
            return actualizado

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Proveedor no encontrado",
    )
