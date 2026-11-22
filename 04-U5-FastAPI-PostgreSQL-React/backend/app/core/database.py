import os
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/foodstore",
)

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)


def create_db_and_tables() -> None:
    """Crea las tablas declaradas con SQLModel si todavía no existen."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Entrega una sesión independiente por cada request y garantiza su cierre."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
