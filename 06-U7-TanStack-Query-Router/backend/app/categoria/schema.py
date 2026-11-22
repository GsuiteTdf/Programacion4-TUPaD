from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

NombreCategoria = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=120),
]
DescripcionCategoria = Annotated[
    str,
    StringConstraints(strip_whitespace=True, max_length=500),
]


class CategoriaBase(BaseModel):
    nombre: NombreCategoria
    descripcion: DescripcionCategoria = ""


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    pass


class CategoriaPublic(CategoriaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
