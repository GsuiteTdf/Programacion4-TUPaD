# Backend — Trabajo Práctico Unidad 7

API FastAPI con persistencia PostgreSQL mediante SQLModel para las entidades `Categoria`, `Producto` y `ProductoCategoria`.

## Requisitos

- Python 3.12 o superior
- PostgreSQL

## Instalación

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Base de datos

Crear una base PostgreSQL y configurar `.env`:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/foodstore_u7
```

Las tablas se crean automáticamente al iniciar FastAPI mediante `SQLModel.metadata.create_all(engine)`.

## Ejecutar

Desde la carpeta `backend/`:

```bash
python -m fastapi dev app/main.py
```

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Categorías

- `GET /categorias/`
- `GET /categorias/{id}`
- `POST /categorias/`
- `PUT /categorias/{id}`
- `DELETE /categorias/{id}`

### Productos

- `GET /productos/`
- `GET /productos/{id}`
- `POST /productos/`
- `PUT /productos/{id}`
- `DELETE /productos/{id}`

### ProductoCategoria

- `POST /productos/{id}/categorias`
- `GET /productos/{id}/categorias`
- `DELETE /productos/{id}/categorias/{categoria_id}`

El archivo `productos.http` demuestra el CRUD de Producto y los endpoints de la relación ProductoCategoria, incluidos los casos de error (404, 409 y 422). Se puede ejecutar más de una vez: al final elimina los datos de prueba.

## Reglas implementadas

- `precio_base` no puede ser negativo (422).
- El nombre de la categoría es único, sin distinguir mayúsculas ni espacios extremos (409), como indica el UML.
- Un producto no puede asociarse dos veces a la misma categoría (409).
- Un id inexistente devuelve 404.
- Al eliminar una categoría o un producto, primero se eliminan sus filas en `producto_categoria` (con `session.flush()`) y luego el registro, para no violar las claves foráneas.
