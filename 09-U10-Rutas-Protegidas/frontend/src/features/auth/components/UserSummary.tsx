import type { UsuarioAuth } from '../types/auth.types'
export function UserSummary({ user }: { user: UsuarioAuth }) {
  return (
    <div className="ml-2 border-l border-slate-200 pl-3 text-right text-sm dark:border-slate-700">
      <p className="font-semibold text-slate-800 dark:text-slate-100">{user.nombre} {user.apellido}</p>
      <p className="text-xs text-slate-500 dark:text-slate-400">{user.roles.join(', ')}</p>
    </div>
  )
}
