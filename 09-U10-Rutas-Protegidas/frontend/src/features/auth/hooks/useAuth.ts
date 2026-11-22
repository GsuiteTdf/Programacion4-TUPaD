import { useAuthStore } from '../store/authStore'
export function useAuth() {
  const user = useAuthStore((state) => state.user)
  const checking = useAuthStore((state) => state.checking)
  const login = useAuthStore((state) => state.login)
  const logout = useAuthStore((state) => state.logout)
  const checkAuth = useAuthStore((state) => state.checkAuth)
  return { user, checking, login, logout, checkAuth, isAdmin: user?.roles.includes('admin') ?? false }
}
