# Backend - TP Unidad 6

API REST de **Food Store** con FastAPI, SQLModel y PostgreSQL.

## Estructura

```text
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   └── database.py
│   ├── categoria/
│   │   ├── router.py
│   │   ├── model.py
│   │   ├── schema.py
│   │   ├── repository.py
│   │   └── service.py
│   ├── producto/
│   │   ├── router.py
│   │   ├── model.py
│   │   ├── schema.py
│   │   ├── repository.py
│   │   └── service.py
│   └── producto_categoria/
│       ├── router.py
│       ├── model.py
│       ├── schema.py
│       ├── repository.py
│       └── service.py
├── tests/
│   ├── categorias.http
│   └── productos.http
├── requirements.txt
└── .env
```

Se respeta la separación **Router → Service → Repository → Model**, con schemas Pydantic como contratos HTTP.

## Base de datos

El TP usa PostgreSQL y SQLModel. Crear una base llamada `foodstore`:

```sql
CREATE DATABASE foodstore;
```

El archivo `.env` incluido usa la configuración local de ejemplo:

```text
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/foodstore
```

Si tu usuario, contraseña o puerto son distintos, editar ese valor antes de iniciar.

## Instalación y ejecución

Desde `backend/`:

```bash
python -m venv .venv
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m fastapi dev app/main.py
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python -m fastapi dev app/main.py
```

Servidor: `http://localhost:8000`  
Swagger: `http://localhost:8000/docs`

## CORS

Se habilitan `http://localhost:5173` (origen por defecto de Vite) y `http://127.0.0.1:5173` para evitar problemas si el frontend se abre mediante la dirección loopback numérica.

## Modelos

### Categoria
- `id: int`
- `nombre: str`
- `descripcion: str`

### Producto
- `id: int`
- `nombre: str`
- `descripcion: str`
- `precio_base: str`
- `imagen_url: list[str]` persistida como JSON
- `disponible: bool`

### ProductoCategoria
- `producto_id: int`
- `categoria_id: int`

La tabla asociativa usa ambos IDs como clave primaria y claves foráneas reales.

## REST Client

- `tests/categorias.http`: pruebas del CRUD de Categorías.
- `tests/productos.http`: pruebas del CRUD de Productos y ProductoCategoria, como exige la entrega. Usa variables de respuesta de REST Client para capturar IDs reales y no depender de IDs fijos ni del orden de ejecución respecto de `categorias.http`.
