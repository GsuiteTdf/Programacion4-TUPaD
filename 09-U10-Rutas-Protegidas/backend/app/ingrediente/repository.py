from sqlmodel import Session, func, select

from app.core.repository import Repository

from .model import Ingrediente


class IngredienteRepository(Repository[Ingrediente]):
    def __init__(self, session: Session):
        super().__init__(session, Ingrediente)

    def get_by_id(self, entity_id: int) -> Ingrediente | None:
        return self.session.exec(
            select(Ingrediente).where(Ingrediente.id == entity_id, Ingrediente.deleted_at.is_(None))
        ).first()

    def list_ordered(self) -> list[Ingrediente]:
        return list(
            self.session.exec(
                select(Ingrediente).where(Ingrediente.deleted_at.is_(None)).order_by(Ingrediente.id)
            ).all()
        )

    def find_by_normalized_name(self, nombre: str) -> Ingrediente | None:
        statement = select(Ingrediente).where(
            Ingrediente.deleted_at.is_(None),
            func.lower(func.trim(Ingrediente.nombre)) == nombre.strip().lower(),
        )
        return self.session.exec(statement).first()
