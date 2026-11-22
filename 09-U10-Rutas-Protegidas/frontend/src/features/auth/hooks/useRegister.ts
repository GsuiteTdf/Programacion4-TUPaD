import { useMutation } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { api, apiErrorMessage } from '@/shared/api/api'
import { useNotificationStore } from '@/store/notificationStore'
import type { RegisterInput, UsuarioAuth } from '../types/auth.types'

export function useRegister() {
  const navigate = useNavigate()
  const showNotification = useNotificationStore((state) => state.showNotification)
  const mutation = useMutation({
    mutationFn: async (input: RegisterInput) => (await api.post<UsuarioAuth>('/api/v1/auth/register', input)).data,
    onSuccess: () => {
      showNotification('Cuenta creada correctamente')
      navigate('/login', { replace: true, state: { registered: true } })
    },
    onError: (error) => showNotification(apiErrorMessage(error)),
  })
  return { register: mutation.mutateAsync, isPending: mutation.isPending, error: mutation.error ? apiErrorMessage(mutation.error) : null }
}
