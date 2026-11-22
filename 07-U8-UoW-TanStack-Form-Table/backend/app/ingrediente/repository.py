from sqlmodel import Session, select

from app.core.repository import Repository
from .model import Ingrediente


class IngredienteRepository(Repository[Ingrediente]):
    def __init__(self, session: Session):
        super().__init__(session, Ingrediente)

    def list_ordered(self) -> list[Ingrediente]:
        return list(self.session.exec(select(Ingrediente).order_by(Ingrediente.id)).all())
