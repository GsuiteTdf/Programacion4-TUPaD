from sqlmodel import Field, SQLModel


class Producto(SQLModel, table=True):
    """Entidad persistente de Producto en PostgreSQL."""

    __tablename__ = "productos"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, max_length=120)
    descripcion: str = Field(default="", max_length=500)
    precio: float = Field(ge=0)
