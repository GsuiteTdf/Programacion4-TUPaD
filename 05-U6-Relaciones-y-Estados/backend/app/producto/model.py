from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, max_length=120)
    descripcion: str = Field(default="", max_length=500)
    precio_base: str = Field(max_length=50)
    imagen_url: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False),
    )
    disponible: bool = Field(default=True)
