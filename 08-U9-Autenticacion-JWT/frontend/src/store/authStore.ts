import { create } from 'zustand'
import { createJSONStorage, persist } from 'zustand/middleware'
import { axiosInstance } from '../api/axiosInstance'
import type { LoginCredentials, UsuarioAuth } from '../types/auth.types'

interface AuthState {
  user: UsuarioAuth | null
  isCheckingSession: boolean
  login: (
    email: LoginCredentials['email'],
    password: LoginCredentials['password'],
  ) => Promise<UsuarioAuth>
  logout: () => Promise<void>
  checkSession: () => Promise<void>
  clearSession: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isCheckingSession: true,
      login: async (email, password) => {
        const body = new URLSearchParams({ username: email, password })
        await axiosInstance.post('/api/v1/auth/token', body, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        })
        const { data } = await axiosInstance.get<UsuarioAuth>('/api/v1/auth/me')
        set({ user: data, isCheckingSession: false })
        return data
      },
      logout: async () => {
        try {
          await axiosInstance.post('/api/v1/auth/logout')
        } finally {
          set({ user: null, isCheckingSession: false })
        }
      },
      checkSession: async () => {
        set({ isCheckingSession: true })
        try {
          const { data } = await axiosInstance.get<UsuarioAuth>('/api/v1/auth/me')
          set({ user: data, isCheckingSession: false })
        } catch {
          set({ user: null, isCheckingSession: false })
        }
      },
      clearSession: () => set({ user: null, isCheckingSession: false }),
    }),
    {
      name: 'foodstore-auth',
      storage: createJSONStorage(() => sessionStorage),
      partialize: (state) => ({ user: state.user }),
    },
  ),
)
