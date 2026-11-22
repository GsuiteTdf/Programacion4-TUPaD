from datetime import datetime, timezone

from sqlalchemy import Index, text
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Ingrediente(SQLModel, table=True):
    """Ingrediente del catálogo (CRUD de la Unidad 8, ahora protegido por roles).

    Usa borrado lógico como Categoria y Producto: DELETE completa deleted_at.
    """

    __tablename__ = "ingredientes"
    # Nombre único entre los ingredientes activos (RN-10 opcional de la Unidad 8).
    __table_args__ = (
        Index(
            "uq_ingredientes_nombre_activo",
            "nombre",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=120)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    deleted_at: datetime | None = Field(default=None)
