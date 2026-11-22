import type { Categoria, CategoriaInput } from '../types/categoria'
import { API_URL, apiError, networkError } from './api'

export async function getCategorias(): Promise<Categoria[]> {
  try {
    const response = await fetch(`${API_URL}/categorias/`)
    if (!response.ok) throw await apiError(response)
    return (await response.json()) as Categoria[]
  } catch (error) {
    throw networkError(error)
  }
}

export async function createCategoria(data: CategoriaInput): Promise<Categoria> {
  try {
    const response = await fetch(`${API_URL}/categorias/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!response.ok) throw await apiError(response)
    return (await response.json()) as Categoria
  } catch (error) {
    throw networkError(error)
  }
}

export async function updateCategoria(id: number, data: CategoriaInput): Promise<Categoria> {
  try {
    const response = await fetch(`${API_URL}/categorias/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!response.ok) throw await apiError(response)
    return (await response.json()) as Categoria
  } catch (error) {
    throw networkError(error)
  }
}

export async function deleteCategoria(id: number): Promise<void> {
  try {
    const response = await fetch(`${API_URL}/categorias/${id}`, { method: 'DELETE' })
    if (!response.ok) throw await apiError(response)
  } catch (error) {
    throw networkError(error)
  }
}
