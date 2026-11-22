# Frontend - Food Store

Pantalla de Productos construida con **React + TypeScript + Vite + Tailwind CSS 4**.

## Alcance de la Unidad 5

Este frontend es **solo maquetado**:

- no consume la API;
- no usa `useState`, `useEffect` ni otros hooks;
- utiliza productos hardcodeados en `App.tsx`;
- pasa datos a componentes hijos mediante props tipados;
- renderiza listas con `.map()` y una `key` única;
- aplica estilos directamente en JSX mediante clases utility-first de Tailwind CSS 4.

## Estructura

```text
frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── ProductoCard.tsx
│   │   ├── ProductoList.tsx
│   │   ├── ProductoForm.tsx
│   │   └── Footer.tsx
│   ├── types/
│   │   └── producto.ts
│   ├── App.tsx
│   ├── index.css
│   └── main.tsx
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Instalación y ejecución

Desde la carpeta `frontend`:

```bash
pnpm install
pnpm dev
```

Para verificar compilación de TypeScript y build de producción:

```bash
pnpm build
```

Tailwind CSS 4 está configurado mediante `@tailwindcss/vite` y se importa desde `src/index.css` con:

```css
@import "tailwindcss";
```


## pnpm 11

El proyecto incluye `pnpm-workspace.yaml` con `allowBuilds` para `esbuild`. Esto permite que pnpm 11 ejecute el script de instalación requerido por Vite/esbuild sin bloquear `pnpm install` o `pnpm dev`.
