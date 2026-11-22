import type { Ingrediente, IngredienteInput } from '../types/ingrediente'
import { API_URL, apiError, networkError } from './api'

export async function getIngredientes(): Promise<Ingrediente[]> {
  try {
    const response = await fetch(`${API_URL}/ingredientes`)
    if (!response.ok) throw await apiError(response)
    return (await response.json()) as Ingrediente[]
  } catch (error) {
    throw networkError(error)
  }
}

export async function createIngrediente(data: IngredienteInput): Promise<Ingrediente> {
  try {
    const response = await fetch(`${API_URL}/ingredientes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!response.ok) throw await apiError(response)
    return (await response.json()) as Ingrediente
  } catch (error) {
    throw networkError(error)
  }
}

export async function updateIngrediente(id: number, data: IngredienteInput): Promise<Ingrediente> {
  try {
    const response = await fetch(`${API_URL}/ingredientes/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!response.ok) throw await apiError(response)
    return (await response.json()) as Ingrediente
  } catch (error) {
    throw networkError(error)
  }
}

export async function deleteIngrediente(id: number): Promise<void> {
  try {
    const response = await fetch(`${API_URL}/ingredientes/${id}`, { method: 'DELETE' })
    if (!response.ok) throw await apiError(response)
  } catch (error) {
    throw networkError(error)
  }
}
