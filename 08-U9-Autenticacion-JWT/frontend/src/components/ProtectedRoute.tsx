import type { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { LoadingState } from './LoadingState'

interface ProtectedRouteProps {
  children: ReactNode
  allowedRoles?: string[]
}

export function ProtectedRoute({ children, allowedRoles }: ProtectedRouteProps) {
  const user = useAuthStore((state) => state.user)
  const isCheckingSession = useAuthStore((state) => state.isCheckingSession)

  if (isCheckingSession) return <LoadingState message="Comprobando sesión..." />
  if (!user) return <Navigate to="/login" replace />
  if (allowedRoles && !allowedRoles.some((role) => user.roles.includes(role))) {
    return <Navigate to="/unauthorized" replace />
  }
  return <>{children}</>
}
