import { NavLink, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

export function Navbar() {
  const user = useAuthStore((state) => state.user)
  const logout = useAuthStore((state) => state.logout)
  const navigate = useNavigate()
  const isAdmin = user?.roles.includes('admin') ?? false

  return (
    <header className="border-b border-slate-200 bg-white shadow-sm">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-5 px-5 py-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-sky-700">Programación IV · U9</p>
          <h1 className="text-xl font-bold text-slate-900">Food Store</h1>
        </div>
        {user ? (
          <div className="flex flex-wrap items-center justify-end gap-2">
            <nav className="flex gap-1">
              <NavLink className={({isActive}) => `rounded-lg px-3 py-2 text-sm font-semibold ${isActive ? 'bg-sky-700 text-white' : 'text-slate-600 hover:bg-slate-100'}`} to="/categories">Categorías</NavLink>
              <NavLink className={({isActive}) => `rounded-lg px-3 py-2 text-sm font-semibold ${isActive ? 'bg-sky-700 text-white' : 'text-slate-600 hover:bg-slate-100'}`} to="/products">Productos</NavLink>
              {isAdmin && <NavLink className={({isActive}) => `rounded-lg px-3 py-2 text-sm font-semibold ${isActive ? 'bg-sky-700 text-white' : 'text-slate-600 hover:bg-slate-100'}`} to="/admin/users">Usuarios</NavLink>}
            </nav>
            <div className="ml-2 border-l pl-3 text-right text-sm">
              <p className="font-semibold text-slate-800">{user.nombre} {user.apellido}</p>
              <p className="text-xs text-slate-500">{user.roles.join(', ')}</p>
            </div>
            <button
              className="rounded-lg bg-slate-800 px-3 py-2 text-sm font-semibold text-white"
              onClick={async () => { await logout(); navigate('/login', { replace: true }) }}
            >
              Cerrar sesión
            </button>
          </div>
        ) : (
          <nav className="flex gap-2">
            <NavLink to="/login" className="rounded-lg px-3 py-2 text-sm font-semibold text-slate-600">Ingresar</NavLink>
            <NavLink to="/register" className="rounded-lg bg-sky-700 px-3 py-2 text-sm font-semibold text-white">Registrarse</NavLink>
          </nav>
        )}
      </div>
    </header>
  )
}
