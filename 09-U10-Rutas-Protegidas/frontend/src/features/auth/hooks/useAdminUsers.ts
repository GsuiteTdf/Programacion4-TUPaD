import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api, apiErrorMessage } from '@/shared/api/api'
import { useNotificationStore } from '@/store/notificationStore'
import type { AdminUser } from '../types/auth.types'

export function useAdminUsers() {
  const queryClient = useQueryClient()
  const showNotification = useNotificationStore((state) => state.showNotification)
  const query = useQuery({
    queryKey: ['admin-users'],
    queryFn: async () => (await api.get<AdminUser[]>('/api/v1/auth/admin/usuarios')).data,
  })
  const mutation = useMutation({
    mutationFn: async ({ id, active }: { id: number; active: boolean }) => {
      const action = active ? 'activar' : 'desactivar'
      return (await api.post<AdminUser>(`/api/v1/auth/admin/usuarios/${id}/${action}`)).data
    },
    onSuccess: async (_, variables) => {
      await queryClient.invalidateQueries({ queryKey: ['admin-users'] })
      showNotification(variables.active ? 'Usuario activado' : 'Usuario desactivado')
    },
    onError: (error) => showNotification(apiErrorMessage(error)),
  })
  return {
    users: query.data ?? [],
    isLoading: query.isPending,
    error: query.isError ? apiErrorMessage(query.error) : null,
    refetch: query.refetch,
    setUserActive: mutation.mutate,
    isUpdating: mutation.isPending,
  }
}
