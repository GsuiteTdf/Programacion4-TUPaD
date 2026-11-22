# Trabajo Práctico Integrador - Unidad 6

**Materia:** Programación IV  
**Alumno:** Gastón Cejas  
**Proyecto:** Food Store - CRUD Categorías + CRUD Productos

Aplicación Full Stack construida con:

- **Backend:** FastAPI + SQLModel + PostgreSQL + Pydantic.
- **Frontend:** React + TypeScript + Vite + Tailwind CSS 4.
- **Integración:** CRUD completo de Categorías mediante `fetch` nativo.
- **Persistencia:** Categorías, Productos y relaciones ProductoCategoria en base de datos.

## Estructura de la entrega

El archivo ZIP contiene directamente:

```text
├── backend/
├── frontend/
└── README.md
```

El frontend implementa el CRUD de Categorías de punta a punta. Los CRUD de Producto y ProductoCategoria se demuestran mediante REST Client en `backend/tests/productos.http`.

## Ejecución rápida

1. Configurar PostgreSQL y el backend siguiendo `backend/README.md`.
2. Levantar FastAPI en `http://localhost:8000`.
3. Instalar y ejecutar el frontend siguiendo `frontend/README.md`.
4. Abrir `http://localhost:5173`.

El backend habilita CORS para `http://localhost:5173` y `http://127.0.0.1:5173`.

## Decisiones de modelado

- `ProductoCategoria` se implementa como tabla asociativa persistente con clave primaria compuesta (`producto_id`, `categoria_id`) y claves foráneas a Producto y Categoria. Esto representa directamente el modelo provisto por la guía.
- `Producto.imagen_url` es `list[str]` y se persiste en una columna JSON, conforme a la aclaración docente del foro.
- `precio_base` se conserva como `str` porque ese es el tipo indicado expresamente en el cuadro de modelos del TP.
