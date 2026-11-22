import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api, apiErrorMessage } from '@/shared/api/api'
import { useNotificationStore } from '@/store/notificationStore'
import { useAuthStore } from '@/features/auth'
import type { Producto, ProductoInput } from '../types/product.types'

export function useProducts() {
  const queryClient = useQueryClient()
  const showNotification = useNotificationStore((state) => state.showNotification)
  const isAdmin = useAuthStore((state) => state.user?.roles.includes('admin') ?? false)
  const query = useQuery({ queryKey: ['productos'], queryFn: async () => (await api.get<Producto[]>('/productos/')).data })
  const invalidate = () => queryClient.invalidateQueries({ queryKey: ['productos'] })
  const createMutation = useMutation({ mutationFn: async (data: ProductoInput) => (await api.post<Producto>('/productos/', data)).data, onSuccess: async () => { await invalidate(); showNotification('Producto creado') }, onError: (e) => showNotification(apiErrorMessage(e)) })
  const updateMutation = useMutation({ mutationFn: async ({ id, data }: { id: number; data: ProductoInput }) => (await api.put<Producto>(`/productos/${id}`, data)).data, onSuccess: async () => { await invalidate(); showNotification('Producto actualizado') }, onError: (e) => showNotification(apiErrorMessage(e)) })
  const deleteMutation = useMutation({ mutationFn: async (id: number) => { await api.delete(`/productos/${id}`) }, onSuccess: async () => { await invalidate(); showNotification('Producto eliminado') }, onError: (e) => showNotification(apiErrorMessage(e)) })
  return { products: query.data ?? [], isLoading: query.isPending, error: query.isError ? apiErrorMessage(query.error) : null, refetch: query.refetch, isAdmin, createProduct: createMutation.mutateAsync, updateProduct: (id: number, data: ProductoInput) => updateMutation.mutateAsync({ id, data }), deleteProduct: deleteMutation.mutateAsync, isSaving: createMutation.isPending || updateMutation.isPending, deletingId: deleteMutation.isPending ? deleteMutation.variables : null }
}
