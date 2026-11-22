from datetime import datetime, timezone

from sqlalchemy import Column, Index, Text, text
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"
    # UML: nombre {UQ}. Con borrado lógico, la unicidad se exige solo entre las
    # categorías activas: así se puede volver a crear el nombre de una categoría eliminada.
    __table_args__ = (
        Index(
            "uq_categorias_nombre_activa",
            "nombre",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    descripcion: str = Field(default="", sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    deleted_at: datetime | None = Field(default=None)
