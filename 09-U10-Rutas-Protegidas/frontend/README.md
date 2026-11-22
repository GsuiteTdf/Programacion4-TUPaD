# Food Store — Unidad 10

Frontend React + TypeScript refactorizado desde la Unidad 9 con **arquitectura por features**, rutas protegidas y estado global de interfaz con Zustand.

## Estructura

```text
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── store/
│   │   ├── types/
│   │   ├── pages/
│   │   └── index.ts
│   ├── categories/   # components, hooks, types, pages, index.ts
│   ├── products/     # components, hooks, types, pages, index.ts
│   └── ingredients/  # components, hooks, types, pages, index.ts
├── shared/
│   ├── components/   # Navbar, UnauthorizedPage, Toast y estados reutilizables
│   └── api/          # api.ts + setupInterceptors.ts
├── store/            # themeStore + notificationStore
├── routes/           # AppRouter + ProtectedRoute
├── App.tsx
└── main.tsx
```

## Reglas de arquitectura

- Cada feature expone su API pública mediante `index.ts`.
- Los imports entre features usan únicamente el barrel y el alias `@/`.
- `useCategories`, `useProducts` y `useIngredients` encapsulan Axios + TanStack Query.
- Las páginas no llaman Axios ni `useQuery`/`useMutation` directamente.
- `ProtectedRoute` usa `<Outlet />` y valida sesión/rol.
- `authStore` **no usa persist**: la sesión se recupera con `/api/v1/auth/me` al iniciar.
- `themeStore` usa `persist` con el nombre `theme-storage`.
- `notificationStore` controla un `Toast` global que se oculta a los 3 segundos.
- `setupInterceptors.ts` limpia sesión ante 401 y muestra “Acceso denegado” ante 403 sin cerrar la sesión.

## Instalación y ejecución

```bash
pnpm install
pnpm dev
```

Build de verificación:

```bash
pnpm build
```

El backend de la Unidad 9 debe estar disponible en `http://localhost:8000` con autenticación por cookie HttpOnly.

> La feature `ingredients/` se conserva porque la consigna de la Unidad 10 la exige expresamente junto a `useIngredients` y la ruta `/ingredients`.
