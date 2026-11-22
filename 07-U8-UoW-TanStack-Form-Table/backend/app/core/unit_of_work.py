from types import TracebackType
from typing import Self

from sqlmodel import Session

from app.core.database import engine


class UnitOfWork:
    """Context manager transaccional.

    Una unidad de trabajo abre una Session, confirma una sola vez al finalizar
    correctamente y revierte todos los cambios si ocurre una excepción.
    """

    session: Session

    def __enter__(self) -> Self:
        self.session = Session(engine, expire_on_commit=False)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool:
        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        finally:
            self.session.close()
        return False
