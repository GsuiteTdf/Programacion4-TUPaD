import { NavLink, useLocation } from 'react-router-dom'

const links = [
  { to: '/categorias', label: 'Categorías' },
  { to: '/productos', label: 'Productos' },
  { to: '/ingredientes', label: 'Ingredientes' },
]

export function Navbar() {
  // La ruta "/" muestra CategoriasPage: se marca también la pestaña Categorías.
  const { pathname } = useLocation()

  return (
    <header className="border-b border-slate-200 bg-white shadow-sm">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-sky-700">
            Programación IV · U8
          </p>
          <h1 className="text-xl font-bold text-slate-900">Food Store</h1>
        </div>
        <nav className="flex gap-2">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `rounded-lg px-3 py-2 text-sm font-semibold transition ${
                  isActive || (link.to === '/categorias' && pathname === '/')
                    ? 'bg-sky-700 text-white'
                    : 'text-slate-600 hover:bg-slate-100'
                }`
              }
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  )
}
