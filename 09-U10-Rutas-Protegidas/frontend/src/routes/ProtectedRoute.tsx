import { Navigate, Outlet } from 'react-router-dom'
import { useAuthStore } from '@/features/auth'
import { LoadingState } from '@/shared/components/LoadingState'

export function ProtectedRoute({ allowedRoles }: { allowedRoles?: string[] }) {
  const user = useAuthStore((state) => state.user)
  const checking = useAuthStore((state) => state.checking)
  if (checking) return <main className="mx-auto max-w-6xl px-5 py-8"><LoadingState message="Verificando sesión…" /></main>
  if (!user) return <Navigate to="/login" replace />
  if (allowedRoles && !allowedRoles.some((role) => user.roles.includes(role))) return <Navigate to="/unauthorized" replace />
  return <Outlet />
}
