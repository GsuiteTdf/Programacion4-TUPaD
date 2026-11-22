from typing import Annotated

from pydantic import StringConstraints
from sqlmodel import Field, SQLModel

NombreProducto = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=150),
]


class ProductoBase(SQLModel):
    nombre: NombreProducto
    descripcion: str = ""
    precio_base: float = Field(ge=0)
    imagenes_url: list[str] = Field(default_factory=list)
    disponible: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


class ProductoPublic(ProductoBase):
    id: int
    # Nombres de las categorías activas del producto (la principal primero).
    categorias: list[str] = []


class ProductoCategoriaCreate(SQLModel):
    categoria_id: int = Field(gt=0)
    es_principal: bool = False


class ProductoCategoriaPublic(SQLModel):
    producto_id: int
    categoria_id: int
    es_principal: bool
