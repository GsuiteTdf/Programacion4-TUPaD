from fastapi import APIRouter, Path, Query, status

from . import schemas, services


router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


@router.post(
    "/",
    response_model=schemas.ProveedorRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un proveedor",
    description=(
        "Crea un proveedor nuevo. El código debe ser único y los datos se "
        "validan con Pydantic antes de llegar al servicio."
    ),
)
def alta_proveedor(
    proveedor: schemas.ProveedorCreate,
) -> schemas.ProveedorRead:
    """Registra un proveedor y devuelve el recurso creado."""
    return services.crear(proveedor)


@router.get(
    "/",
    response_model=list[schemas.ProveedorRead],
    status_code=status.HTTP_200_OK,
    summary="Listar proveedores",
    description=(
        "Devuelve proveedores con paginación y filtro opcional por estado activo."
    ),
)
def listar_proveedores(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    activo: bool | None = Query(None),
) -> list[schemas.ProveedorRead]:
    """Lista proveedores aplicando paginación y filtro de estado."""
    return services.obtener_todos(skip=skip, limit=limit, activo=activo)


@router.get(
    "/{id}",
    response_model=schemas.ProveedorRead,
    status_code=status.HTTP_200_OK,
    summary="Consultar un proveedor",
    description="Obtiene el detalle de un proveedor por su identificador.",
)
def detalle_proveedor(
    id: int = Path(..., gt=0),
) -> schemas.ProveedorRead:
    """Devuelve un proveedor existente o informa 404 desde el servicio."""
    return services.obtener_por_id(id)


@router.put(
    "/{id}",
    response_model=schemas.ProveedorRead,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un proveedor",
    description=(
        "Reemplaza todos los campos del proveedor. El cuerpo usa ProveedorCreate "
        "porque el PUT definido por la consigna es de reemplazo total."
    ),
)
def actualizar_proveedor(
    proveedor: schemas.ProveedorCreate,
    id: int = Path(..., gt=0),
) -> schemas.ProveedorRead:
    """Reemplaza completamente los datos de un proveedor existente."""
    return services.actualizar_total(id, proveedor)


@router.put(
    "/{id}/desactivar",
    response_model=schemas.ProveedorRead,
    status_code=status.HTTP_200_OK,
    summary="Desactivar un proveedor",
    description=(
        "Realiza la baja lógica del proveedor cambiando activo a false. "
        "No elimina el registro de la lista en memoria."
    ),
)
def desactivar_proveedor(
    id: int = Path(..., gt=0),
) -> schemas.ProveedorRead:
    """Desactiva un proveedor conservando su registro histórico."""
    return services.desactivar(id)
