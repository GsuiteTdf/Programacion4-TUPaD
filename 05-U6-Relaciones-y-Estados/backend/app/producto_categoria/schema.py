from pydantic import BaseModel, ConfigDict, Field


class ProductoCategoriaBase(BaseModel):
    producto_id: int = Field(gt=0)
    categoria_id: int = Field(gt=0)


class ProductoCategoriaCreate(ProductoCategoriaBase):
    pass


class ProductoCategoriaUpdate(ProductoCategoriaBase):
    pass


class ProductoCategoriaPublic(ProductoCategoriaBase):
    model_config = ConfigDict(from_attributes=True)
