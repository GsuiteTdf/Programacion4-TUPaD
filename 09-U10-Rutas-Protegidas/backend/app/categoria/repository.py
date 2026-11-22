from sqlmodel import Session, func, select

from app.core.repository import Repository
from app.producto.model import Producto, ProductoCategoria

from .model import Categoria


class CategoriaRepository(Repository[Categoria]):
    def __init__(self, session: Session):
        super().__init__(session, Categoria)

    def get_by_id(self, entity_id: int) -> Categoria | None:
        return self.session.exec(
            select(Categoria).where(Categoria.id == entity_id, Categoria.deleted_at.is_(None))
        ).first()

    def list_ordered(self) -> list[Categoria]:
        return list(
            self.session.exec(
                select(Categoria).where(Categoria.deleted_at.is_(None)).order_by(Categoria.id)
            ).all()
        )

    def find_by_normalized_name(self, nombre: str) -> Categoria | None:
        statement = select(Categoria).where(
            Categoria.deleted_at.is_(None),
            func.lower(func.trim(Categoria.nombre)) == nombre.strip().lower(),
        )
        return self.session.exec(statement).first()

    def has_products(self, categoria_id: int) -> bool:
        statement = (
            select(ProductoCategoria)
            .join(Producto, Producto.id == ProductoCategoria.producto_id)
            .where(ProductoCategoria.categoria_id == categoria_id, Producto.deleted_at.is_(None))
        )
        return self.session.exec(statement).first() is not None
