from sqlalchemy import Boolean, Column, String
from sqlmodel import Field, SQLModel


class FormaPago(SQLModel, table=True):
    __tablename__ = "formas_pago"

    codigo: str = Field(sa_column=Column(String(30), primary_key=True))
    descripcion: str = Field(max_length=80)
    activo: bool = Field(default=True, sa_column=Column(Boolean, nullable=False, default=True))


class EstadoPedido(SQLModel, table=True):
    __tablename__ = "estados_pedido"

    codigo: str = Field(sa_column=Column(String(20), primary_key=True))
    descripcion: str = Field(max_length=80)
    orden: int
    es_terminal: bool
