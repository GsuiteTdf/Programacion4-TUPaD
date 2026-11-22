import axios from 'axios'

export const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
  headers: { Accept: 'application/json' },
})

// La cookie HttpOnly la adjunta el navegador: este interceptor NO lee ni agrega el JWT.
axiosInstance.interceptors.request.use((config) => config)

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const status = error?.response?.status as number | undefined
    const url = String(error?.config?.url ?? '')
    const excluded = url.includes('/api/v1/auth/token') || url.includes('/api/v1/auth/me')
    const detail = (error?.response?.data as { detail?: unknown } | undefined)?.detail
    // Si un admin desactiva la cuenta, el backend responde 400 en las rutas protegidas:
    // la sesión ya no sirve y se vuelve al login, igual que con un 401.
    const cuentaDesactivada = status === 400 && detail === 'Cuenta de usuario desactivada'
    if ((status === 401 || cuentaDesactivada) && !excluded) {
      const { useAuthStore } = await import('../store/authStore')
      useAuthStore.getState().clearSession()
    }
    return Promise.reject(error)
  },
)

export function apiErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) {
      return detail
        .map((item) => (typeof item?.msg === 'string' ? item.msg : String(item)))
        .join('. ')
    }
    if (!error.response) return 'No se pudo conectar con el backend en localhost:8000'
    return `La API respondió con error ${error.response.status}`
  }
  return error instanceof Error ? error.message : 'Error inesperado'
}
