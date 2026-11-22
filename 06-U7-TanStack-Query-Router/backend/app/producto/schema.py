from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.categoria.schema import CategoriaPublic

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
    descripcion: DescripcionProducto = ""
    precio_base: float = Field(ge=0)
    imagenes_url: list[str] = Field(default_factory=list)
    disponible: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


class ProductoPublic(ProductoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProductoCategoriaCreate(BaseModel):
    categoria_id: int = Field(gt=0)


class ProductoCategoriaPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    producto_id: int
    categoria_id: int


class ProductoCategoriasPublic(BaseModel):
    producto_id: int
    categorias: list[CategoriaPublic]
