# Food Store - Frontend Unidad 8

React + TypeScript + Vite + Tailwind CSS 4.

## TanStack

- Query: `useQuery`, `useMutation`, invalidación de caché.
- Form: `useForm` y `form.Field` con validación.
- Table **v8**: ordenamiento y paginación con `getSortedRowModel` y `getPaginationRowModel`.

## Rutas

La consigna del PDF conserva las rutas en español y el aviso del campus menciona equivalentes en inglés. Se incluyen ambas, apuntando a las mismas páginas:

- `/categorias` y `/categories`
- `/productos` y `/products`
- `/ingredientes` y `/ingredients`

`App.tsx` solo define rutas y renderiza el Navbar.

## Ejecución

```bash
pnpm install
pnpm build
pnpm dev
```

El backend debe estar disponible en `http://localhost:8000`.

## Notas de implementación

- Los modales usan `form.reset(valores, { keepDefaultValues: true })`. Sin esa opción, `reset()` reemplaza los `defaultValues` y en el siguiente render `useForm` vuelve a aplicar los valores vacíos, por lo que el modal de edición se abriría sin datos.
- Si la API responde con error (409, 422, 404), el mensaje del backend se muestra en el modal o sobre la tabla.
