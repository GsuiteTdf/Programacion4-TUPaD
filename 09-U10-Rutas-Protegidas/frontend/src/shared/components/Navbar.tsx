import { NavLink, useNavigate } from 'react-router-dom'
import { UserSummary, useAuth } from '@/features/auth'
import { useThemeStore } from '@/store/themeStore'

const linkClass = ({ isActive }: { isActive: boolean }) => `rounded-lg px-3 py-2 text-sm font-semibold ${isActive ? 'bg-sky-700 text-white' : 'text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800'}`

export function Navbar() {
  const { user, logout, isAdmin } = useAuth()
  const darkMode = useThemeStore((state) => state.darkMode)
  const toggleTheme = useThemeStore((state) => state.toggleTheme)
  const navigate = useNavigate()
  return (
    <header className="border-b border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-950">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-5 px-5 py-4">
        <div><p className="text-xs font-semibold uppercase tracking-[0.2em] text-sky-700">Programación IV · U10</p><h1 className="text-xl font-bold">Food Store</h1></div>
        <div className="flex items-center gap-2">
          <button onClick={toggleTheme} className="rounded-lg border px-3 py-2 text-sm font-semibold dark:border-slate-700" aria-label="Alternar tema">{darkMode ? '☀️ Claro' : '🌙 Oscuro'}</button>
          {user ? <><nav className="flex gap-1"><NavLink className={linkClass} to="/categories">Categorías</NavLink><NavLink className={linkClass} to="/products">Productos</NavLink><NavLink className={linkClass} to="/ingredients">Ingredientes</NavLink>{isAdmin && <NavLink className={linkClass} to="/admin/users">Usuarios</NavLink>}</nav><UserSummary user={user} /><button className="rounded-lg bg-slate-800 px-3 py-2 text-sm font-semibold text-white dark:bg-slate-700" onClick={async () => { await logout(); navigate('/login', { replace: true }) }}>Cerrar sesión</button></> : <nav className="flex gap-2"><NavLink to="/login" className={linkClass}>Ingresar</NavLink><NavLink to="/register" className="rounded-lg bg-sky-700 px-3 py-2 text-sm font-semibold text-white">Registrarse</NavLink></nav>}
        </div>
      </div>
    </header>
  )
}
