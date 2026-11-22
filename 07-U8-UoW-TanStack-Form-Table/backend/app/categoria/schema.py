from typing import Annotated

from pydantic import StringConstraints
from sqlmodel import SQLModel

NombreCategoria = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=100),
]


class CategoriaBase(SQLModel):
    nombre: NombreCategoria
    descripcion: str = ""


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    pass


class CategoriaPublic(CategoriaBase):
    id: int
