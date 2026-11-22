from app.core.unit_of_work import UnitOfWork

from .repository import (
    DetallePedidoRepository,
    PedidoProductoRepository,
    PedidoRepository,
)


class PedidoUnitOfWork(UnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.pedidos = PedidoRepository(self.session)
        self.detalles = DetallePedidoRepository(self.session)
        self.productos = PedidoProductoRepository(self.session)
        return self
