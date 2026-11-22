from typing import Annotated

from pydantic import StringConstraints
from sqlmodel import SQLModel

# RN-10: obligatorio, sin aceptar un nombre compuesto solo por espacios.
NombreIngrediente = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=120),
]


class IngredienteBase(SQLModel):
    nombre: NombreIngrediente


class IngredienteCreate(IngredienteBase):
    pass


class IngredienteUpdate(IngredienteBase):
    pass


class IngredientePublic(IngredienteBase):
    id: int
