from datetime import datetime, timezone

from .exceptions import PedidoNoEncontrado, ProductoNoEncontrado
from .model import DetallePedido, Pedido
from .schema import (
    DetallePedidoPublic,
    PedidoCreate,
    PedidoPublic,
    PedidoUpdate,
)
from .unit_of_work import PedidoUnitOfWork


def _public(uow: PedidoUnitOfWork, pedido: Pedido) -> PedidoPublic:
    detalles = [
        DetallePedidoPublic.model_validate(item)
        for item in uow.detalles.list_by_pedido(pedido.id)
    ]
    return PedidoPublic(
        id=pedido.id,
        fecha=pedido.fecha,
        estado=pedido.estado,
        total=pedido.total,
        detalles=detalles,
    )


class PedidoService:
    def listar(self) -> list[PedidoPublic]:
        with PedidoUnitOfWork() as uow:
            return [_public(uow, pedido) for pedido in uow.pedidos.list_active()]

    def obtener(self, pedido_id: int) -> PedidoPublic:
        with PedidoUnitOfWork() as uow:
            pedido = uow.pedidos.get_active(pedido_id)
            if pedido is None:
                raise PedidoNoEncontrado(pedido_id)
            return _public(uow, pedido)

    def crear(self, data: PedidoCreate) -> PedidoPublic:
        # Toda la operación vive dentro del mismo UoW. Si un detalle falla,
        # __exit__ recibe la excepción y ejecuta rollback de pedido + detalles.
        with PedidoUnitOfWork() as uow:
            pedido = uow.pedidos.create(Pedido(estado="PENDIENTE", total=0))
            total = 0.0

            for item in data.detalles:
                producto = uow.productos.get_by_id(item.producto_id)
                if producto is None:
                    raise ProductoNoEncontrado(item.producto_id)

                precio = float(producto.precio_base)
                uow.detalles.create(
                    DetallePedido(
                        pedido_id=pedido.id,
                        producto_id=producto.id,
                        cantidad=item.cantidad,
                        precio_unitario=precio,
                    )
                )
                total += item.cantidad * precio

            pedido.total = round(total, 2)
            uow.session.add(pedido)
            uow.session.flush()
            return _public(uow, pedido)

    def actualizar_estado(self, pedido_id: int, data: PedidoUpdate) -> PedidoPublic:
        with PedidoUnitOfWork() as uow:
            pedido = uow.pedidos.get_active(pedido_id)
            if pedido is None:
                raise PedidoNoEncontrado(pedido_id)
            pedido.estado = data.estado
            uow.session.add(pedido)
            uow.session.flush()
            return _public(uow, pedido)

    def eliminar(self, pedido_id: int) -> None:
        with PedidoUnitOfWork() as uow:
            pedido = uow.pedidos.get_active(pedido_id)
            if pedido is None:
                raise PedidoNoEncontrado(pedido_id)
            pedido.deleted_at = datetime.now(timezone.utc)
            uow.session.add(pedido)
            uow.session.flush()
