import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api, apiErrorMessage } from '@/shared/api/api'
import { useNotificationStore } from '@/store/notificationStore'
import { useAuthStore } from '@/features/auth'
import type { Categoria, CategoriaInput } from '../types/category.types'

export function useCategories() {
  const queryClient = useQueryClient()
  const showNotification = useNotificationStore((state) => state.showNotification)
  const isAdmin = useAuthStore((state) => state.user?.roles.includes('admin') ?? false)
  const query = useQuery({ queryKey: ['categorias'], queryFn: async () => (await api.get<Categoria[]>('/categorias/')).data })
  const invalidate = () => queryClient.invalidateQueries({ queryKey: ['categorias'] })
  const createMutation = useMutation({ mutationFn: async (data: CategoriaInput) => (await api.post<Categoria>('/categorias/', data)).data, onSuccess: async () => { await invalidate(); showNotification('Categoría creada') }, onError: (e) => showNotification(apiErrorMessage(e)) })
  const updateMutation = useMutation({ mutationFn: async ({ id, data }: { id: number; data: CategoriaInput }) => (await api.put<Categoria>(`/categorias/${id}`, data)).data, onSuccess: async () => { await invalidate(); showNotification('Categoría actualizada') }, onError: (e) => showNotification(apiErrorMessage(e)) })
  const deleteMutation = useMutation({ mutationFn: async (id: number) => { await api.delete(`/categorias/${id}`) }, onSuccess: async () => { await invalidate(); showNotification('Categoría eliminada') }, onError: (e) => showNotification(apiErrorMessage(e)) })
  return { categories: query.data ?? [], isLoading: query.isPending, error: query.isError ? apiErrorMessage(query.error) : null, refetch: query.refetch, isAdmin, createCategory: createMutation.mutateAsync, updateCategory: (id: number, data: CategoriaInput) => updateMutation.mutateAsync({ id, data }), deleteCategory: deleteMutation.mutateAsync, isSaving: createMutation.isPending || updateMutation.isPending, deletingId: deleteMutation.isPending ? deleteMutation.variables : null }
}
