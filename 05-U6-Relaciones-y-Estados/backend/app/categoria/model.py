from sqlmodel import Field, SQLModel


class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, max_length=120)
    descripcion: str = Field(default="", max_length=500)
