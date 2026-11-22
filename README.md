# Programación IV — Trabajos prácticos

Trabajos prácticos de **Programación IV** · Tecnicatura Universitaria en Programación a Distancia (UTN) · 2026.

Recorrido completo de la materia: de Spring Boot y la programación orientada a objetos en Python a aplicaciones **full stack** con **FastAPI + SQLModel + PostgreSQL** en el backend y **React + TypeScript** en el frontend, sumando en cada unidad persistencia, relaciones, gestión de estado del servidor, formularios, tablas, arquitectura Unit of Work, autenticación con JWT y rutas protegidas.

- **Alumno:** Gastón Cejas · TUPaD - UTN
- **Trabajo Práctico Integrador:** [TPI-FoodStore-Programacion4](https://github.com/GsuiteTdf/TPI-FoodStore-Programacion4)

## Contenido

| Carpeta                              | Tema                                    | Tecnologías y conceptos                                                                                         |
| ------------------------------------ | --------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `01-TP1-SpringBoot-Gestion-Pedidos`  | Fundamentos de Spring                   | Java · Spring Boot · Spring Data JPA · H2 · Lombok · DTOs · inyección de dependencias · `@Service`, `@Repository` |
| `02-TPI-POO-Python`                  | Programación orientada a objetos        | Python · clases abstractas (ABC) · `Protocol` · relaciones entre clases · polimorfismo                          |
| `03-U4-FastAPI`                      | Introducción a FastAPI                  | FastAPI · Pydantic v2 · parámetros de ruta y consulta · `HTTPException` · `response_model` · arquitectura modular |
| `04-U5-FastAPI-PostgreSQL-React`     | Persistencia y primer frontend          | SQLModel · PostgreSQL · CRUD persistente · React + TypeScript con Vite · Tailwind CSS 4                          |
| `05-U6-Relaciones-y-Estados`         | Relaciones y estado en React            | Relaciones 1:N y N:N · `useState` / `useEffect` · integración backend–frontend                                  |
| `06-U7-TanStack-Query-Router`        | Estado del servidor y navegación        | TanStack Query (`useQuery`, `useMutation`, invalidación) · React Router · optimización de endpoints             |
| `07-U8-UoW-TanStack-Form-Table`      | Arquitectura del backend y UI de datos  | Unit of Work · Repository · TanStack Form · TanStack Table v8 (orden y paginación)                               |
| `08-U9-Autenticacion-JWT`            | Seguridad                               | JWT en cookie HttpOnly · roles `user` / `admin` · RBAC · Axios con interceptores · borrado lógico                |
| `09-U10-Rutas-Protegidas`            | Arquitectura del frontend               | Organización por features · rutas protegidas por rol · Zustand · backend con módulo de ingredientes             |

Cada carpeta es un proyecto independiente con sus propias instrucciones (`README.md` en la carpeta o en `backend/` y `frontend/`).

## Requisitos generales

| Proyecto                | Requisitos                                         |
| ----------------------- | -------------------------------------------------- |
| Spring Boot (TP1)       | JDK 21 · Gradle Wrapper incluido                   |
| Python / FastAPI        | Python 3.12+ · PostgreSQL (desde la Unidad 5)       |
| Frontends React         | Node.js 20.19+ · pnpm 9+                           |

## Ejecución típica (unidades 5 a 10)

```bash
# Backend
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate  ·  Linux / macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env     # Linux / macOS: cp .env.example .env
uvicorn app.main:app --reload   # el módulo exacto se indica en el README de cada unidad
```

```bash
# Frontend
cd frontend
pnpm install
pnpm dev
```

> Los archivos `.env` no se incluyen en el repositorio: se crean a partir de cada `.env.example`.
