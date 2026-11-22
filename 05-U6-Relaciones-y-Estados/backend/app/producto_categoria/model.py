from sqlmodel import Field, SQLModel


class ProductoCategoria(SQLModel, table=True):
    __tablename__ = "producto_categoria"

    producto_id: int = Field(
        foreign_key="productos.id",
        primary_key=True,
    )
    categoria_id: int = Field(
        foreign_key="categorias.id",
        primary_key=True,
    )
