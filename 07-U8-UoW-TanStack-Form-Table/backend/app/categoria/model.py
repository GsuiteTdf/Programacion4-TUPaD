from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: int | None = Field(default=None, primary_key=True)
    # UML Catálogo: VARCHAR(100), único y obligatorio.
    nombre: str = Field(index=True, unique=True, max_length=100)
    descripcion: str = Field(
        default="",
        sa_column=Column(Text, nullable=False),
    )
