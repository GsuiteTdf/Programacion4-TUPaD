import type { Producto, ProductoInput } from '../types/producto'
import { API_URL, apiError, networkError } from './api'

export async function getProductos(): Promise<Producto[]> {
  try {
    const response = await fetch(`${API_URL}/productos/`)
    if (!response.ok) throw await apiError(response)
    return (await response.json()) as Producto[]
  } catch (error) {
    throw networkError(error)
  }
}

export async function createProducto(data: ProductoInput): Promise<Producto> {
  try {
    const response = await fetch(`${API_URL}/productos/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!response.ok) throw await apiError(response)
    return (await response.json()) as Producto
  } catch (error) {
    throw networkError(error)
  }
}

export async function updateProducto(id: number, data: ProductoInput): Promise<Producto> {
  try {
    const response = await fetch(`${API_URL}/productos/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!response.ok) throw await apiError(response)
    return (await response.json()) as Producto
  } catch (error) {
    throw networkError(error)
  }
}

export async function deleteProducto(id: number): Promise<void> {
  try {
    const response = await fetch(`${API_URL}/productos/${id}`, { method: 'DELETE' })
    if (!response.ok) throw await apiError(response)
  } catch (error) {
    throw networkError(error)
  }
}
