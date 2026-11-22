import { Link, NavLink } from 'react-router-dom'

const navClass = ({ isActive }: { isActive: boolean }) =>
  `rounded-lg px-3 py-2 text-sm font-semibold transition-colors ${
    isActive
      ? 'bg-blue-100 text-blue-800'
      : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
  }`

export const Navbar = () => (
  <header className="border-b border-slate-200 bg-white">
    <nav className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-4">
      <Link to="/categorias" className="text-xl font-bold tracking-tight text-slate-900">
        Food Store
      </Link>

      <div className="flex items-center gap-2">
        <NavLink to="/categorias" className={navClass}>
          Categorías
        </NavLink>
        <NavLink to="/productos" className={navClass}>
          Productos
        </NavLink>
      </div>
    </nav>
  </header>
)
