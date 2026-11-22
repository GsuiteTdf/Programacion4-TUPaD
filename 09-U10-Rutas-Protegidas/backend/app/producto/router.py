from fastapi import APIRouter, Depends, Response, status

from app.core.security import get_current_active_user, require_role

from .schema import ProductoCategoriaCreate, ProductoCategoriaPublic, ProductoCreate, ProductoPublic, ProductoUpdate
from .service import actualizar_producto, asignar_categoria, crear_producto, eliminar_producto, listar_categorias_producto, listar_productos, obtener_producto, quitar_categoria

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/", response_model=list[ProductoPublic], dependencies=[Depends(get_current_active_user)])
def listar() -> list[ProductoPublic]:
    return listar_productos()


@router.get("/{producto_id}", response_model=ProductoPublic, dependencies=[Depends(get_current_active_user)])
def obtener(producto_id: int) -> ProductoPublic:
    return obtener_producto(producto_id)


@router.post("/", response_model=ProductoPublic, status_code=201, dependencies=[Depends(require_role(["admin"]))])
def crear(data: ProductoCreate) -> ProductoPublic:
    return crear_producto(data)


@router.put("/{producto_id}", response_model=ProductoPublic, dependencies=[Depends(require_role(["admin"]))])
def actualizar(producto_id: int, data: ProductoUpdate) -> ProductoPublic:
    return actualizar_producto(producto_id, data)


@router.delete("/{producto_id}", status_code=204, response_model=None, dependencies=[Depends(require_role(["admin"]))])
def eliminar(producto_id: int) -> Response:
    eliminar_producto(producto_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{producto_id}/categorias", response_model=ProductoCategoriaPublic, status_code=201, dependencies=[Depends(require_role(["admin"]))])
def asociar(producto_id: int, data: ProductoCategoriaCreate) -> ProductoCategoriaPublic:
    return asignar_categoria(producto_id, data)


@router.get("/{producto_id}/categorias", response_model=list[ProductoCategoriaPublic], dependencies=[Depends(get_current_active_user)])
def categorias(producto_id: int) -> list[ProductoCategoriaPublic]:
    return listar_categorias_producto(producto_id)


@router.delete("/{producto_id}/categorias/{categoria_id}", status_code=204, response_model=None, dependencies=[Depends(require_role(["admin"]))])
def desasociar(producto_id: int, categoria_id: int) -> Response:
    quitar_categoria(producto_id, categoria_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
