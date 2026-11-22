# Backend - Food Store

API REST persistente para administrar Productos con **FastAPI + SQLModel + PostgreSQL**.

## Arquitectura

```text
backend/
├── main.py
├── app/
│   ├── core/
│   │   └── database.py
│   └── modules/
│       └── productos/
│           ├── model.py
│           ├── schema.py
│           ├── repository.py
│           ├── service.py
│           └── router.py
├── tests/
│   └── productos.http
├── requirements.txt
└── .env.example
```

Flujo principal: **Router → Service → Repository → Model**. Los schemas Pydantic/SQLModel actúan como contratos de entrada y salida.

## Requisitos

- Python 3.12 o superior.
- PostgreSQL en ejecución.
- Una base de datos llamada `foodstore` (o la que indique `DATABASE_URL`).

Ejemplo en PostgreSQL:

```sql
CREATE DATABASE foodstore;
```

## Instalación

Desde la carpeta `backend`:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/foodstore"
uvicorn main:app --reload
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/foodstore"
uvicorn main:app --reload
```

Si no se define `DATABASE_URL`, el proyecto usa por defecto:

```text
postgresql+psycopg://postgres:postgres@localhost:5432/foodstore
```

### Nota sobre `.env.example`

El archivo `.env.example` es únicamente una referencia de configuración. Este TP no agrega una dependencia extra para cargar archivos `.env` automáticamente: `DATABASE_URL` se define como variable de entorno, tal como se muestra arriba.

## Swagger

Con el servidor iniciado:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Reglas implementadas

- Nombre obligatorio, con eliminación de espacios extremos y rechazo de cadenas vacías.
- Precio mayor o igual a cero.
- Nombre único de forma normalizada (sin distinguir mayúsculas y espacios extremos).
- IDs inexistentes devuelven 404.
- Duplicados devuelven 409.
- Validaciones Pydantic devuelven 422.
- POST, PUT y DELETE confirman cambios mediante `Session.commit()`.

## Pruebas

Abrir `tests/productos.http` con REST Client y ejecutar los casos válidos e inválidos. También se incluye `tests/FoodStore_Productos.postman_collection.json` para ejecutar la misma batería desde Postman.
