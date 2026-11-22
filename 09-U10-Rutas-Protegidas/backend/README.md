# Food Store · Unidad 9 · Backend (con ingredientes para la Unidad 10)

> **Versión para probar el frontend de la Unidad 10.** Es el backend entregado en la Unidad 9 más el módulo `app/ingrediente/` (`/ingredientes`). La consigna de la Unidad 9 excluye los ingredientes del modelo, pero la de la Unidad 10 exige la feature `ingredients/` con `useIngredients` y la ruta `/ingredients`: sin este módulo esa página recibe 404. El backend no se entrega en la Unidad 10; esta copia sirve solo para ejecutar el frontend completo.

FastAPI + SQLModel + PostgreSQL con autenticación JWT en cookie HttpOnly, roles `user`/`admin`, RBAC y borrado lógico.

## Preparación

1. Crear PostgreSQL `foodstore_u9`.
2. Copiar `.env.example` a `.env` y reemplazar `DATABASE_URL`, `SECRET_KEY` y, si se desea, las credenciales del admin de prueba.
3. Crear y activar `.venv`.
4. Instalar: `pip install -r requirements.txt`.
5. Ejecutar `python seed.py` para cargar roles `admin`/`user`, los seis estados, formas de pago y el admin opcional.
6. Levantar: `uvicorn app.main:app --reload`.
7. Swagger: `http://localhost:8000/docs`.

## Seguridad

- `POST /api/v1/auth/register`: registro público y rol `user`.
- `POST /api/v1/auth/token`: OAuth2 form (`username` contiene el email), JWT en cookie HttpOnly.
- `POST /api/v1/auth/logout`: elimina la cookie.
- `GET /api/v1/auth/me`: perfil y roles vigentes.
- `/api/v1/auth/admin/usuarios`: administración de usuarios (solo `admin`).
- GET de Categoría/Producto: cualquier usuario autenticado.
- POST/PUT/DELETE de Categoría/Producto/ProductoCategoria: solo `admin`.
- Pedidos: cualquier usuario autenticado (`user` o `admin`) los crea y el `usuario_id` se toma de la sesión. Un `user` solo ve sus propios pedidos (un pedido ajeno responde 404); cambiar el estado y borrar es solo para `admin`.
- Estados de pedido: los seis del catálogo `EstadoPedido` (PENDIENTE, CONFIRMADO, EN_PREP, EN_CAMINO, ENTREGADO, CANCELADO).
- Un admin no puede desactivar su propia cuenta (400).
- `Categoria`, `Producto`, `Pedido` y `Usuario` usan borrado lógico (`deleted_at`). Las tablas de enlace se eliminan físicamente.
- El nombre de categoría es único entre las categorías activas (índice único parcial `WHERE deleted_at IS NULL`): se puede volver a crear el nombre de una categoría eliminada.
- Al borrar lógicamente un producto se eliminan sus filas en `producto_categoria`; una categoría solo se considera "con productos" si alguno está activo.
- `GET /productos/` y `GET /productos/{id}` incluyen `categorias`: los nombres de sus categorías (la principal primero).

## REST Client

- `auth.http`: registro, cookie, `/me`, 403, logout y administración.
- `categorias.http`, `productos.http`, `pedidos.http`, `ingredientes.http`: operaciones protegidas.

El archivo `.env` NO forma parte de la entrega; sólo se incluye `.env.example`.

## Usuario administrador de prueba

`seed.py` crea el admin definido en `SEED_ADMIN_EMAIL` y `SEED_ADMIN_PASSWORD`. El email debe tener un dominio válido: dominios reservados como `.local` o `.test` son rechazados por la validación `EmailStr` y el usuario no podría iniciar sesión. Los `.http` usan `admin@foodstore.com` / `Admin123!`.

Si ya existía una base creada con una versión anterior de este proyecto, conviene recrearla: `create_all` no modifica tablas existentes (por ejemplo, el índice único parcial de categorías).

## Ingredientes (agregado para la Unidad 10)

- `GET /ingredientes` y `GET /ingredientes/{id}`: cualquier usuario autenticado.
- `POST /ingredientes`, `PUT /ingredientes/{id}` y `DELETE /ingredientes/{id}`: solo `admin` (un `user` recibe 403).
- Nombre obligatorio, sin aceptar solo espacios (422) y único entre los ingredientes activos, sin distinguir mayúsculas (409).
- `DELETE` hace borrado lógico (`deleted_at`), como en Categoría y Producto.
- `ingredientes.http` demuestra todos los casos.
