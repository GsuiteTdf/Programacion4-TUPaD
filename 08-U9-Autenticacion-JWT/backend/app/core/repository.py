from typing import Generic, TypeVar

from sqlmodel import Session, SQLModel, select

ModelT = TypeVar("ModelT", bound=SQLModel)


class Repository(Generic[ModelT]):
    """CRUD de persistencia sin control transaccional.

    El Repository agrega, consulta, elimina y puede hacer flush para obtener IDs,
    pero nunca ejecuta commit() ni rollback(). Es responsabilidad del Unit of Work.
    """

    def __init__(self, session: Session, model: type[ModelT]):
        self.session = session
        self.model = model

    def get_by_id(self, entity_id: int) -> ModelT | None:
        return self.session.get(self.model, entity_id)

    def list_all(self) -> list[ModelT]:
        return list(self.session.exec(select(self.model)).all())

    def create(self, entity: ModelT) -> ModelT:
        self.session.add(entity)
        self.session.flush()
        return entity

    def delete(self, entity: ModelT) -> None:
        self.session.delete(entity)
