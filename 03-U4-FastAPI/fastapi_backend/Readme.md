# FastAPI Backend - TP Integrador Unidad 4: Proveedores

Alumno: Cejas Gaston A.
Proyecto base de **Programación IV** extendido con el módulo `proveedor/`.
El trabajo aplica los contenidos de la Unidad 4: FastAPI, Pydantic v2,
parámetros de ruta y consulta, arquitectura modular, códigos HTTP,
`HTTPException`, `response_model` y pruebas con REST Client.

Los datos se almacenan **en memoria** mientras el servidor está en ejecución,
tal como establece la consigna. No utiliza base de datos ni persistencia externa.

## Requisitos

- Python 3.12 o superior.
- Dependencias declaradas en `requirements.txt`.
- Extensión REST Client de VS Code recomendada para ejecutar los archivos `.http`.

## Instalación

Desde la carpeta raíz `fastapi_backend`:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

Ingresar al proyecto integrador y levantar FastAPI:

```bash
cd u1_ej_8_integrador
fastapi dev app/main.py
```

La API queda disponible en:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI: `http://127.0.0.1:8000/openapi.json`

## Módulo Proveedores

El módulo se encuentra en:

```text
u1_ej_8_integrador/
└── app/
    └── modules/
        └── proveedor/
            ├── __init__.py
            ├── routers.py
            ├── schemas.py
            └── services.py
```

La separación de responsabilidades sigue el patrón del proyecto base:

- `routers.py`: endpoints, parámetros HTTP, `response_model` y códigos de estado.
- `schemas.py`: modelos Pydantic y validaciones de entrada/salida.
- `services.py`: lógica de negocio y almacenamiento en memoria.

## Endpoints de Proveedores

| Método | Endpoint | Código | Descripción |
| --- | --- | ---: | --- |
| POST | `/proveedores/` | 201 | Crear un proveedor |
| GET | `/proveedores/` | 200 | Listar proveedores |
| GET | `/proveedores/{id}` | 200 | Consultar un proveedor |
| PUT | `/proveedores/{id}` | 200 | Reemplazo total de un proveedor |
| PUT | `/proveedores/{id}/desactivar` | 200 | Desactivación lógica |

El listado acepta:

- `skip`: entero, mínimo `0`, por defecto `0`.
- `limit`: entero entre `1` y `50`, por defecto `10`.
- `activo`: `true`, `false` u omitido para no filtrar.

## Schemas Pydantic

Se implementan:

- `ProveedorBase`
- `ProveedorCreate`
- `ProveedorUpdate`
- `ProveedorRead`

`ProveedorUpdate` conserva todos sus campos opcionales, como pide la consigna.
El endpoint `PUT /proveedores/{id}` usa `ProveedorCreate` porque el contrato del
trabajo establece un **reemplazo total**, por lo que exige todos los campos
obligatorios del proveedor.

## Reglas de negocio

El backend implementa las reglas RN-01 a RN-05:

1. El código es obligatorio y no puede quedar vacío (`422`).
2. El código es único (`409 Conflict` si se duplica).
3. La razón social es obligatoria y tiene mínimo 3 caracteres (`422`).
4. Un id positivo inexistente devuelve `404 Not Found` al consultar, actualizar
   o desactivar.
5. Un proveedor ya desactivado no puede desactivarse nuevamente (`409 Conflict`).

Los parámetros de ruta también se validan con `Path(gt=0)`, por lo que un id
no positivo es rechazado automáticamente por FastAPI/Pydantic con `422`.

## Pruebas REST Client

El archivo:

```text
u1_ej_8_integrador/tests/proveedores.http
```

demuestra los cinco endpoints, paginación, filtros y escenarios `200`, `201`,
`404`, `409` y `422`. Incluye además casos de validación automática de
parámetros `Path` y `Query`.

## Estructura relevante

```text
fastapi_backend/
├── requirements.txt
├── Readme.md
└── u1_ej_8_integrador/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   └── modules/
    │       ├── categoria/
    │       ├── producto/
    │       └── proveedor/
    └── tests/
        ├── test_api.http
        └── proveedores.http
```

## Nota sobre el almacenamiento

El contenido de proveedores se reinicia al detener el servidor porque el
trabajo de esta unidad utiliza listas en memoria, sin persistencia externa.
