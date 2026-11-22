import { create } from 'zustand'
import { api } from '@/shared/api/api'
import type { LoginCredentials, UsuarioAuth } from '../types/auth.types'

interface AuthState {
  user: UsuarioAuth | null
  checking: boolean
  login: (email: LoginCredentials['email'], password: LoginCredentials['password']) => Promise<UsuarioAuth>
  logout: () => Promise<void>
  checkAuth: () => Promise<void>
  clearSession: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  checking: true,
  login: async (email, password) => {
    const body = new URLSearchParams({ username: email, password })
    await api.post('/api/v1/auth/token', body, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    const { data } = await api.get<UsuarioAuth>('/api/v1/auth/me')
    set({ user: data, checking: false })
    return data
  },
  logout: async () => {
    try { await api.post('/api/v1/auth/logout') }
    finally { set({ user: null, checking: false }) }
  },
  checkAuth: async () => {
    set({ checking: true })
    try {
      const { data } = await api.get<UsuarioAuth>('/api/v1/auth/me')
      set({ user: data, checking: false })
    } catch {
      set({ user: null, checking: false })
    }
  },
  clearSession: () => set({ user: null, checking: false }),
}))
