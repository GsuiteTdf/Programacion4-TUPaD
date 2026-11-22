from sqlmodel import Session, func, select

from app.core.repository import Repository
from app.producto.model import ProductoCategoria

from .model import Categoria


class CategoriaRepository(Repository[Categoria]):
    def __init__(self, session: Session):
        super().__init__(session, Categoria)

    def list_ordered(self) -> list[Categoria]:
        return list(self.session.exec(select(Categoria).order_by(Categoria.id)).all())

    def find_by_normalized_name(self, nombre: str) -> Categoria | None:
        statement = select(Categoria).where(
            func.lower(func.trim(Categoria.nombre)) == nombre.strip().lower()
        )
        return self.session.exec(statement).first()

    def has_products(self, categoria_id: int) -> bool:
        statement = select(ProductoCategoria).where(
            ProductoCategoria.categoria_id == categoria_id
        )
        return self.session.exec(statement).first() is not None
