import { api } from '@/shared/api/api'
import { useNotificationStore } from '@/store/notificationStore'
import { useAuthStore } from '@/features/auth'

let interceptorInstalled = false

export function setupInterceptors() {
  if (interceptorInstalled) return
  interceptorInstalled = true

  api.interceptors.response.use(
    (response) => response,
    (error) => {
      const status = error?.response?.status as number | undefined
      const url = String(error?.config?.url ?? '')
      const detail = (error?.response?.data as { detail?: unknown } | undefined)?.detail
      const excluded401 = url.includes('/api/v1/auth/token') || url.includes('/api/v1/auth/me')
      const disabledAccount = status === 400 && detail === 'Cuenta de usuario desactivada'

      if ((status === 401 || disabledAccount) && !excluded401) {
        useAuthStore.getState().clearSession()
      } else if (status === 403) {
        useNotificationStore.getState().showNotification('Acceso denegado')
      }

      return Promise.reject(error)
    },
  )
}
