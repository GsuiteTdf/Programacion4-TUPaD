import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { ErrorState } from '../components/ErrorState'
import { LoadingState } from '../components/LoadingState'
import { getAdminUsers, setUserActive } from '../services/admin'
import { useAuthStore } from '../store/authStore'

export function AdminUsersPage() {
  const currentUserId = useAuthStore((state) => state.user?.id)
  const qc = useQueryClient()
  const query = useQuery({ queryKey: ['admin-users'], queryFn: getAdminUsers })
  const mutation = useMutation({
    mutationFn: ({ id, active }: { id: number; active: boolean }) => setUserActive(id, active),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin-users'] }),
  })
  if (query.isPending) return <LoadingState message="Cargando usuarios..." />
  if (query.isError)
    return <ErrorState message={query.error.message} onRetry={() => void query.refetch()} />
  return (
    <main className="mx-auto max-w-6xl px-5 py-8">
      <h2 className="text-3xl font-bold">Administración de usuarios</h2>
      <div className="mt-6 overflow-x-auto rounded-xl border bg-white">
        <table className="w-full text-left">
          <thead className="bg-slate-100 text-sm">
            <tr>
              <th className="p-3">Usuario</th>
              <th className="p-3">Email</th>
              <th className="p-3">Roles</th>
              <th className="p-3">Estado</th>
              <th className="p-3">Acción</th>
            </tr>
          </thead>
          <tbody>
            {query.data.map((u) => (
              <tr key={u.id} className="border-t">
                <td className="p-3">
                  {u.nombre} {u.apellido}
                </td>
                <td className="p-3">{u.email}</td>
                <td className="p-3">{u.roles.join(', ')}</td>
                <td className="p-3">{u.activo ? 'Activo' : 'Desactivado'}</td>
                <td className="p-3">
                  {u.id === currentUserId ? (
                    <span className="text-sm text-slate-500">Tu cuenta</span>
                  ) : (
                    <button
                      disabled={mutation.isPending}
                      onClick={() => mutation.mutate({ id: u.id, active: !u.activo })}
                      className={`rounded px-3 py-1.5 text-sm font-semibold text-white ${u.activo ? 'bg-red-700' : 'bg-emerald-700'}`}
                    >
                      {u.activo ? 'Desactivar' : 'Activar'}
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {mutation.isError && (
        <div className="mt-4">
          <ErrorState message={mutation.error.message} />
        </div>
      )}
    </main>
  )
}
