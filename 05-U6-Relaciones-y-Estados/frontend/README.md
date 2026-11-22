# Frontend - TP Unidad 6

Frontend de Food Store con **React + TypeScript + Tailwind CSS 4**.

## Funcionalidad

El CRUD de Categorías funciona contra la API FastAPI real:

- Listar categorías: `GET /categorias/`
- Crear: `POST /categorias/`
- Editar: `PUT /categorias/{id}`
- Eliminar: `DELETE /categorias/{id}`

Se utiliza únicamente **fetch nativo**. No se usa Axios.

## Hooks

`App.tsx` usa:

- `useState` para categorías, apertura del modal, categoría seleccionada, carga y errores.
- `useEffect` para ejecutar el `GET /categorias/` al montar la aplicación.

`CategoriaModal.tsx` usa únicamente el custom hook `useForm` para los campos del formulario. El estado `guardando` se mantiene en `App.tsx`, respetando la conclusión de la guía de que los demás componentes deben permanecer funcionales puros salvo el uso de `useForm` en el modal.

## Tipado

- `src/types/categoria.ts`: `Categoria` y `CategoriaInput`.
- `src/hooks/useForm.ts`: custom hook tipado para el formulario del modal.
- `src/types/producto.ts`: `Producto` con los campos definidos por el backend.
- Todas las props de los componentes están tipadas.
- No se usa `any`.

## Instalación

Requiere Node.js y pnpm. Desde `frontend/`:

```bash
pnpm install
pnpm build
pnpm dev
```

Abrir `http://localhost:5173`.

El backend debe estar iniciado en `http://localhost:8000`.

## pnpm 11

Se incluye `pnpm-workspace.yaml` con autorización explícita del build de `esbuild`, y `pnpm-lock.yaml` para mantener las versiones reproducibles.
