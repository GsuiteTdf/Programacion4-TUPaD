from sqlmodel import Session, select

from app.core.repository import Repository
from app.producto.model import Producto

from .model import DetallePedido, Pedido


class PedidoRepository(Repository[Pedido]):
    def __init__(self, session: Session):
        super().__init__(session, Pedido)

    def list_active(self, usuario_id: int | None = None) -> list[Pedido]:
        statement = select(Pedido).where(Pedido.deleted_at.is_(None))
        if usuario_id is not None:
            statement = statement.where(Pedido.usuario_id == usuario_id)
        return list(self.session.exec(statement.order_by(Pedido.id)).all())

    def get_active(self, pedido_id: int) -> Pedido | None:
        return self.session.exec(select(Pedido).where(Pedido.id == pedido_id, Pedido.deleted_at.is_(None))).first()


class DetallePedidoRepository(Repository[DetallePedido]):
    def __init__(self, session: Session):
        super().__init__(session, DetallePedido)

    def list_by_pedido(self, pedido_id: int) -> list[DetallePedido]:
        return list(self.session.exec(select(DetallePedido).where(DetallePedido.pedido_id == pedido_id).order_by(DetallePedido.producto_id)).all())


class PedidoProductoRepository(Repository[Producto]):
    def __init__(self, session: Session):
        super().__init__(session, Producto)

    def get_by_id(self, entity_id: int) -> Producto | None:
        return self.session.exec(select(Producto).where(Producto.id == entity_id, Producto.deleted_at.is_(None))).first()
