import { apiErrorMessage, axiosInstance } from '../api/axiosInstance'
import type { Categoria, CategoriaInput } from '../types/categoria'

export async function getCategorias(): Promise<Categoria[]> {
  try { return (await axiosInstance.get<Categoria[]>('/categorias/')).data }
  catch (error) { throw new Error(apiErrorMessage(error)) }
}

export async function createCategoria(data: CategoriaInput): Promise<Categoria> {
  try { return (await axiosInstance.post<Categoria>('/categorias/', data)).data }
  catch (error) { throw new Error(apiErrorMessage(error)) }
}

export async function updateCategoria(id: number, data: CategoriaInput): Promise<Categoria> {
  try { return (await axiosInstance.put<Categoria>(`/categorias/${id}`, data)).data }
  catch (error) { throw new Error(apiErrorMessage(error)) }
}

export async function deleteCategoria(id: number): Promise<void> {
  try { await axiosInstance.delete(`/categorias/${id}`) }
  catch (error) { throw new Error(apiErrorMessage(error)) }
}
