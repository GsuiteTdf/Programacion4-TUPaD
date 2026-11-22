# Food Store · Unidad 9 · Frontend

React + TypeScript + Vite + Tailwind + TanStack Query/Form/Table, con Axios y Zustand.

## Instalación

```bash
pnpm install
pnpm build
pnpm dev
```

El backend debe ejecutarse en `http://localhost:8000` con CORS `allow_credentials=True`.

## Seguridad

- Axios usa `withCredentials: true`.
- El JWT **no se almacena ni se lee en JavaScript**: viaja en cookie HttpOnly.
- El interceptor de respuesta limpia el AuthStore ante 401 (excepto login y `/auth/me`) y también ante el 400 «Cuenta de usuario desactivada», para que un usuario desactivado por el admin vuelva al login.
- Zustand `persist` guarda únicamente el objeto `user` en `sessionStorage`, nunca el token.
- `/categories` y `/products`: requieren sesión.
- `/admin/users`: requiere rol `admin`.
- Los botones Crear/Editar/Eliminar del catálogo se muestran solamente a `admin`.
- Login y registro usan TanStack Form.
- La tabla de productos muestra las categorías de cada producto (campo `categorias` que envía el backend).
- En `/admin/users` no se ofrece desactivar la propia cuenta del admin.

## Usuario administrador de prueba

`python seed.py` (backend) crea `admin@foodstore.com` / `Admin123!` con los valores de `.env.example`.
