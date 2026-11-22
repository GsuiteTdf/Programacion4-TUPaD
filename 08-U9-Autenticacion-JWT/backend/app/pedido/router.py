from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.security import SessionDep, get_current_active_user, require_role
from app.modules.usuarios.repository import UsuarioRolRepository

from .exceptions import PedidoNoEncontrado, ProductoNoEncontrado
from .schema import PedidoCreate, PedidoPublic, PedidoUpdate
from .service import PedidoService

router = APIRouter(prefix="/pedidos", tags=["pedidos"])
service = PedidoService()


def _traducir_error(exc: Exception) -> HTTPException:
    if isinstance(exc, PedidoNoEncontrado):
        return HTTPException(status_code=404, detail="Pedido no encontrado")
    if isinstance(exc, ProductoNoEncontrado):
        return HTTPException(status_code=404, detail=f"Producto {exc.producto_id} no encontrado")
    return HTTPException(status_code=422, detail=str(exc))


def filtro_propietario(session: SessionDep, current_user=Depends(get_current_active_user)) -> int | None:
    """None si el usuario es admin (ve todos los pedidos); si no, su id (solo ve los propios)."""
    roles = UsuarioRolRepository(session).role_names_for_user(current_user.id)
    return None if "admin" in roles else current_user.id


@router.get("", response_model=list[PedidoPublic])
def listar(usuario_id: int | None = Depends(filtro_propietario)) -> list[PedidoPublic]:
    return service.listar(usuario_id)


@router.get("/{pedido_id}", response_model=PedidoPublic)
def obtener(pedido_id: int, usuario_id: int | None = Depends(filtro_propietario)) -> PedidoPublic:
    try:
        return service.obtener(pedido_id, usuario_id)
    except (PedidoNoEncontrado, ProductoNoEncontrado) as exc:
        raise _traducir_error(exc) from exc


@router.post("", response_model=PedidoPublic, status_code=201)
def crear(data: PedidoCreate, current_user=Depends(require_role(["user", "admin"]))) -> PedidoPublic:
    try:
        return service.crear(data, current_user.id)
    except (PedidoNoEncontrado, ProductoNoEncontrado) as exc:
        raise _traducir_error(exc) from exc


@router.put("/{pedido_id}", response_model=PedidoPublic)
def actualizar(pedido_id: int, data: PedidoUpdate, _=Depends(require_role(["admin"]))) -> PedidoPublic:
    try:
        return service.actualizar_estado(pedido_id, data)
    except (PedidoNoEncontrado, ProductoNoEncontrado) as exc:
        raise _traducir_error(exc) from exc


@router.delete("/{pedido_id}", status_code=204, response_model=None)
def eliminar(pedido_id: int, _=Depends(require_role(["admin"]))) -> Response:
    try:
        service.eliminar(pedido_id)
    except (PedidoNoEncontrado, ProductoNoEncontrado) as exc:
        raise _traducir_error(exc) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
