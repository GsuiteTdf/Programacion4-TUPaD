# Frontend — Trabajo Práctico Unidad 7

Aplicación React + TypeScript creada con Vite. El CRUD de Categorías consume FastAPI mediante TanStack Query y la navegación se resuelve con React Router.

## Instalación

```bash
pnpm install
```

## Desarrollo

```bash
pnpm dev
```

## Verificación de TypeScript y build

```bash
pnpm build
```

La aplicación espera:

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

## Estructura relevante

```text
src/
├── components/
│   ├── Navbar.tsx
│   ├── CategoriaCard.tsx
│   ├── CategoriaList.tsx
│   └── CategoriaModal.tsx
├── pages/
│   ├── CategoriasPage.tsx
│   └── ProductsPage.tsx
├── services/
│   └── categoria.ts
├── types/
│   ├── categoria.ts
│   └── producto.ts
├── App.tsx
├── main.tsx
└── index.css
```

`CategoriasPage.tsx` utiliza `useQuery` para el listado y `useMutation` para alta, edición y baja. Cada mutación invalida `queryKey: ['categorias']`. `App.tsx` sólo renderiza el Navbar y define las rutas `/categorias` y `/productos`.
