from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.security import get_current_active_user
from app.modules.usuarios.model import Rol

from .model import EstadoPedido, FormaPago

router = APIRouter(prefix="/api/v1/catalogos", tags=["catalogos"])


@router.get("/roles", response_model=list[Rol])
def roles(
    session: Session = Depends(get_session),
    _=Depends(get_current_active_user),
) -> list[Rol]:
    return list(session.exec(select(Rol).order_by(Rol.id)).all())


@router.get("/formas-pago", response_model=list[FormaPago])
def formas_pago(
    session: Session = Depends(get_session),
    _=Depends(get_current_active_user),
) -> list[FormaPago]:
    return list(session.exec(select(FormaPago).order_by(FormaPago.codigo)).all())


@router.get("/estados-pedido", response_model=list[EstadoPedido])
def estados_pedido(
    session: Session = Depends(get_session),
    _=Depends(get_current_active_user),
) -> list[EstadoPedido]:
    return list(session.exec(select(EstadoPedido).order_by(EstadoPedido.orden)).all())
