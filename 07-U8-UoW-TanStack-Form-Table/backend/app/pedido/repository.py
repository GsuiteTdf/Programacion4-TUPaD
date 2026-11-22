from sqlmodel import Session, select

from app.core.repository import Repository
from app.producto.model import Producto

from .model import DetallePedido, Pedido


class PedidoRepository(Repository[Pedido]):
    def __init__(self, session: Session):
        super().__init__(session, Pedido)

    def list_active(self) -> list[Pedido]:
        statement = select(Pedido).where(Pedido.deleted_at.is_(None)).order_by(Pedido.id)
        return list(self.session.exec(statement).all())

    def get_active(self, pedido_id: int) -> Pedido | None:
        statement = select(Pedido).where(
            Pedido.id == pedido_id,
            Pedido.deleted_at.is_(None),
        )
        return self.session.exec(statement).first()


class DetallePedidoRepository(Repository[DetallePedido]):
    def __init__(self, session: Session):
        super().__init__(session, DetallePedido)

    def list_by_pedido(self, pedido_id: int) -> list[DetallePedido]:
        statement = select(DetallePedido).where(
            DetallePedido.pedido_id == pedido_id
        ).order_by(DetallePedido.producto_id)
        return list(self.session.exec(statement).all())


class PedidoProductoRepository(Repository[Producto]):
    def __init__(self, session: Session):
        super().__init__(session, Producto)
