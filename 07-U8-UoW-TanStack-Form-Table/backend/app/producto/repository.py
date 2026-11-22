from sqlmodel import Session, select

from app.core.repository import Repository
from app.pedido.model import DetallePedido

from .model import Producto, ProductoCategoria


class ProductoRepository(Repository[Producto]):
    def __init__(self, session: Session):
        super().__init__(session, Producto)

    def list_ordered(self) -> list[Producto]:
        return list(self.session.exec(select(Producto).order_by(Producto.id)).all())

    def has_pedidos(self, producto_id: int) -> bool:
        # Incluye pedidos dados de baja lógica: sus detalles siguen en la base.
        statement = select(DetallePedido).where(DetallePedido.producto_id == producto_id)
        return self.session.exec(statement).first() is not None


class ProductoCategoriaRepository(Repository[ProductoCategoria]):
    def __init__(self, session: Session):
        super().__init__(session, ProductoCategoria)

    def get_link(self, producto_id: int, categoria_id: int) -> ProductoCategoria | None:
        return self.session.get(ProductoCategoria, (producto_id, categoria_id))

    def list_by_producto(self, producto_id: int) -> list[ProductoCategoria]:
        statement = select(ProductoCategoria).where(
            ProductoCategoria.producto_id == producto_id
        ).order_by(ProductoCategoria.categoria_id)
        return list(self.session.exec(statement).all())

    def unset_principal(self, producto_id: int) -> None:
        for link in self.list_by_producto(producto_id):
            if link.es_principal:
                link.es_principal = False
                self.session.add(link)

    def delete_by_producto(self, producto_id: int) -> None:
        for link in self.list_by_producto(producto_id):
            self.session.delete(link)
        self.session.flush()
