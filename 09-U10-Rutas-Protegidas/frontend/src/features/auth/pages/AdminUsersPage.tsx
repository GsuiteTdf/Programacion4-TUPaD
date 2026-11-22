import { ErrorState } from '@/shared/components/ErrorState'
import { LoadingState } from '@/shared/components/LoadingState'
import { useAdminUsers } from '../hooks/useAdminUsers'
import { useAuth } from '../hooks/useAuth'

export function AdminUsersPage() {
  const { user } = useAuth()
  const { users, isLoading, error, refetch, setUserActive, isUpdating } = useAdminUsers()
  if (isLoading) return <LoadingState message="Cargando usuarios…" />
  if (error) return <ErrorState message={error} onRetry={() => void refetch()} />
  return (
    <main className="mx-auto max-w-6xl px-5 py-8">
      <h2 className="text-3xl font-bold">Administración de usuarios</h2>
      <div className="mt-6 overflow-x-auto rounded-xl border bg-white dark:border-slate-700 dark:bg-slate-900">
        <table className="w-full text-left">
          <thead className="bg-slate-100 text-sm dark:bg-slate-800"><tr><th className="p-3">Usuario</th><th className="p-3">Email</th><th className="p-3">Roles</th><th className="p-3">Estado</th><th className="p-3">Acción</th></tr></thead>
          <tbody>{users.map((u) => <tr key={u.id} className="border-t dark:border-slate-700"><td className="p-3">{u.nombre} {u.apellido}</td><td className="p-3">{u.email}</td><td className="p-3">{u.roles.join(', ')}</td><td className="p-3">{u.activo ? 'Activo' : 'Desactivado'}</td><td className="p-3">{u.id === user?.id ? <span className="text-sm text-slate-500">Tu cuenta</span> : <button disabled={isUpdating} onClick={() => setUserActive({ id: u.id, active: !u.activo })} className={`rounded px-3 py-1.5 text-sm font-semibold text-white ${u.activo ? 'bg-red-700' : 'bg-emerald-700'}`}>{u.activo ? 'Desactivar' : 'Activar'}</button>}</td></tr>)}</tbody>
        </table>
      </div>
    </main>
  )
}
