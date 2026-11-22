import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api, apiErrorMessage } from '@/shared/api/api'
import { useNotificationStore } from '@/store/notificationStore'
import { useAuthStore } from '@/features/auth'
import type { Ingrediente, IngredienteInput } from '../types/ingredient.types'

export function useIngredients() {
  const queryClient = useQueryClient()
  const showNotification = useNotificationStore((state) => state.showNotification)
  const isAdmin = useAuthStore((state) => state.user?.roles.includes('admin') ?? false)
  const query = useQuery({ queryKey: ['ingredientes'], queryFn: async () => (await api.get<Ingrediente[]>('/ingredientes')).data })
  const invalidate = () => queryClient.invalidateQueries({ queryKey: ['ingredientes'] })
  const createMutation = useMutation({ mutationFn: async (data: IngredienteInput) => (await api.post<Ingrediente>('/ingredientes', data)).data, onSuccess: async () => { await invalidate(); showNotification('Ingrediente creado') }, onError: (e) => showNotification(apiErrorMessage(e)) })
  const updateMutation = useMutation({ mutationFn: async ({ id, data }: { id: number; data: IngredienteInput }) => (await api.put<Ingrediente>(`/ingredientes/${id}`, data)).data, onSuccess: async () => { await invalidate(); showNotification('Ingrediente actualizado') }, onError: (e) => showNotification(apiErrorMessage(e)) })
  const deleteMutation = useMutation({ mutationFn: async (id: number) => { await api.delete(`/ingredientes/${id}`) }, onSuccess: async () => { await invalidate(); showNotification('Ingrediente eliminado') }, onError: (e) => showNotification(apiErrorMessage(e)) })
  return { ingredients: query.data ?? [], isLoading: query.isPending, error: query.isError ? apiErrorMessage(query.error) : null, refetch: query.refetch, isAdmin, createIngredient: createMutation.mutateAsync, updateIngredient: (id: number, data: IngredienteInput) => updateMutation.mutateAsync({ id, data }), deleteIngredient: deleteMutation.mutateAsync, isSaving: createMutation.isPending || updateMutation.isPending, deletingId: deleteMutation.isPending ? deleteMutation.variables : null }
}
