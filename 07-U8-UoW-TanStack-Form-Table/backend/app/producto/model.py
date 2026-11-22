from sqlalchemy import Boolean, Column, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import Field, SQLModel


class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id: int | None = Field(default=None, primary_key=True)
    # Longitud alineada con el paquete Catálogo del UML.
    nombre: str = Field(index=True, max_length=150)
    descripcion: str = Field(default="", sa_column=Column(Text, nullable=True))
    precio_base: float = Field(ge=0)
    imagenes_url: list[str] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(String), nullable=False),
    )
    disponible: bool = Field(
        default=True,
        sa_column=Column(Boolean, nullable=False, default=True),
    )


class ProductoCategoria(SQLModel, table=True):
    __tablename__ = "producto_categoria"

    producto_id: int = Field(foreign_key="productos.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categorias.id", primary_key=True)
    # Atributo del link model presente en el UML.
    es_principal: bool = Field(default=False)
