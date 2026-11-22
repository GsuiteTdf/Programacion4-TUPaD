from sqlmodel import Session, select

from app.core.repository import Repository

from .model import Producto, ProductoCategoria


class ProductoRepository(Repository[Producto]):
    def __init__(self, session: Session):
        super().__init__(session, Producto)

    def get_by_id(self, entity_id: int) -> Producto | None:
        return self.session.exec(
            select(Producto).where(Producto.id == entity_id, Producto.deleted_at.is_(None))
        ).first()

    def list_ordered(self) -> list[Producto]:
        return list(
            self.session.exec(
                select(Producto).where(Producto.deleted_at.is_(None)).order_by(Producto.id)
            ).all()
        )

    def nombres_categorias(self, producto_id: int) -> list[str]:
        from app.categoria.model import Categoria

        statement = (
            select(Categoria.nombre)
            .join(ProductoCategoria, ProductoCategoria.categoria_id == Categoria.id)
            .where(ProductoCategoria.producto_id == producto_id, Categoria.deleted_at.is_(None))
            .order_by(ProductoCategoria.es_principal.desc(), Categoria.nombre)
        )
        return list(self.session.exec(statement).all())


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
