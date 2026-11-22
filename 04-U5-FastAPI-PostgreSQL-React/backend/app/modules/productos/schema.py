from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


NombreProducto = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=120),
]
DescripcionProducto = Annotated[
    str,
    StringConstraints(strip_whitespace=True, max_length=500),
]


class ProductoBase(BaseModel):
    nombre: NombreProducto
    descripcion: DescripcionProducto
    precio: float = Field(ge=0)


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    """PUT reemplaza completamente los campos editables del producto."""


class ProductoPublic(ProductoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
