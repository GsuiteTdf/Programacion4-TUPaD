from typing import Annotated

from pydantic import EmailStr, StringConstraints
from sqlmodel import SQLModel

Nombre = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)]
Password = Annotated[str, StringConstraints(min_length=8, max_length=72)]


class UserCreate(SQLModel):
    nombre: Nombre
    apellido: Nombre
    email: EmailStr
    celular: str | None = None
    password: Password


class UserPublic(SQLModel):
    id: int
    nombre: str
    apellido: str
    email: EmailStr
    celular: str | None = None
    roles: list[str]


class AdminUserPublic(UserPublic):
    activo: bool
