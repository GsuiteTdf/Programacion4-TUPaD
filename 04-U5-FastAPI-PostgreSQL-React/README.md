# Trabajo Práctico Integrador - Unidad 5

**Materia:** Programación IV  
**Alumno:** Gastón Cejas  
**Proyecto:** Food Store - Gestor de Productos con FastAPI, SQLModel, PostgreSQL, React, TypeScript y Tailwind CSS 4

La entrega contiene dos proyectos independientes:

- `backend/`: API REST persistente con FastAPI + SQLModel + PostgreSQL.
- `frontend/`: maquetado de Productos con React + TypeScript + Tailwind CSS 4.

Cada carpeta incluye su propio `README.md` con instrucciones de instalación y ejecución.


## Alcance de la migración

La guía de la Unidad 5 define este trabajo como **Gestor de Productos** y fija para el dominio `Producto` los campos `id`, `nombre`, `descripcion` y `precio`. Por ese motivo, esta entrega migra ese gestor a PostgreSQL con SQLModel y conserva exactamente ese contrato. Los módulos de otros ejercicios o trabajos previos que no forman parte del Gestor de Productos no se incorporan a esta entrega.

## Compatibilidad con pnpm 11

El frontend incluye `pnpm-workspace.yaml` con autorización explícita para el script de instalación de `esbuild`, necesario para que `pnpm install` y `pnpm dev` funcionen con los controles de seguridad de pnpm 11.
