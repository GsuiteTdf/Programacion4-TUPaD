from fastapi import APIRouter, HTTPException, Response, status

from .exceptions import PedidoNoEncontrado, ProductoNoEncontrado
from .schema import PedidoCreate, PedidoPublic, PedidoUpdate
from .service import PedidoService

router = APIRouter(prefix="/pedidos", tags=["pedidos"])
service = PedidoService()


def _traducir_error(exc: Exception) -> HTTPException:
    if isinstance(exc, PedidoNoEncontrado):
        return HTTPException(status_code=404, detail="Pedido no encontrado")
    if isinstance(exc, ProductoNoEncontrado):
        return HTTPException(
            status_code=404,
            detail=f"Producto {exc.producto_id} no encontrado",
        )
    return HTTPException(status_code=422, detail=str(exc))


@router.get("", response_model=list[PedidoPublic])
def listar() -> list[PedidoPublic]:
    return service.listar()


@router.get("/{pedido_id}", response_model=PedidoPublic)
def obtener(pedido_id: int) -> PedidoPublic:
    try:
        return service.obtener(pedido_id)
    except (PedidoNoEncontrado, ProductoNoEncontrado) as exc:
        raise _traducir_error(exc) from exc


@router.post("", response_model=PedidoPublic, status_code=status.HTTP_201_CREATED)
def crear(data: PedidoCreate) -> PedidoPublic:
    try:
        return service.crear(data)
    except (PedidoNoEncontrado, ProductoNoEncontrado) as exc:
        raise _traducir_error(exc) from exc


@router.put("/{pedido_id}", response_model=PedidoPublic)
def actualizar(pedido_id: int, data: PedidoUpdate) -> PedidoPublic:
    try:
        return service.actualizar_estado(pedido_id, data)
    except (PedidoNoEncontrado, ProductoNoEncontrado) as exc:
        raise _traducir_error(exc) from exc


@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def eliminar(pedido_id: int) -> Response:
    try:
        service.eliminar(pedido_id)
    except (PedidoNoEncontrado, ProductoNoEncontrado) as exc:
        raise _traducir_error(exc) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
