from datetime import datetime
from typing import Literal

from pydantic import model_validator
from sqlmodel import Field, SQLModel

# Los seis estados del catálogo EstadoPedido del UML (cargados por seed.py).
EstadoPedido = Literal["PENDIENTE", "CONFIRMADO", "EN_PREP", "EN_CAMINO", "ENTREGADO", "CANCELADO"]


class DetallePedidoCreate(SQLModel):
    producto_id: int = Field(gt=0)
    cantidad: int = Field(ge=1)


class DetallePedidoPublic(SQLModel):
    pedido_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float


class PedidoCreate(SQLModel):
    detalles: list[DetallePedidoCreate] = Field(min_length=1)

    @model_validator(mode="after")
    def productos_sin_repetir(self):
        ids = [detalle.producto_id for detalle in self.detalles]
        if len(ids) != len(set(ids)):
            raise ValueError("Un producto no puede repetirse dentro del mismo pedido")
        return self


class PedidoUpdate(SQLModel):
    estado: EstadoPedido


class PedidoPublic(SQLModel):
    id: int
    usuario_id: int
    fecha: datetime
    estado: EstadoPedido
    total: float
    detalles: list[DetallePedidoPublic]
