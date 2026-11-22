# Food Store · Unidad 9 · Backend

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
- `categorias.http`, `productos.http`, `pedidos.http`: operaciones protegidas.

El archivo `.env` NO forma parte de la entrega; sólo se incluye `.env.example`.

## Usuario administrador de prueba

`seed.py` crea el admin definido en `SEED_ADMIN_EMAIL` y `SEED_ADMIN_PASSWORD`. El email debe tener un dominio válido: dominios reservados como `.local` o `.test` son rechazados por la validación `EmailStr` y el usuario no podría iniciar sesión. Los `.http` usan `admin@foodstore.com` / `Admin123!`.

Si ya existía una base creada con una versión anterior de este proyecto, conviene recrearla: `create_all` no modifica tablas existentes (por ejemplo, el índice único parcial de categorías).
