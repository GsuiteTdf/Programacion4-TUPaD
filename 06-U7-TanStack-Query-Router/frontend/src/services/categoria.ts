import type { Categoria, CategoriaInput } from '../types/categoria'

const API_URL = 'http://localhost:8000/categorias'

// fetch lanza TypeError cuando no hay conexión con el backend: se traduce a un mensaje claro.
const solicitar = async (url: string, init?: RequestInit): Promise<Response> => {
  try {
    return await fetch(url, init)
  } catch {
    throw new Error(
      'No se pudo conectar con la API. Verificá que el backend esté iniciado en http://localhost:8000.',
    )
  }
}

const obtenerMensajeError = async (response: Response, fallback: string) => {
  try {
    const data: unknown = await response.json()
    if (typeof data === 'object' && data !== null && 'detail' in data) {
      const detail = (data as { detail?: unknown }).detail
      if (typeof detail === 'string' && detail.trim().length > 0) {
        return detail
      }
      // 422 de Pydantic: detail es una lista de errores con su campo "msg".
      if (Array.isArray(detail)) {
        const mensajes = detail
          .map((item: unknown) =>
            typeof item === 'object' && item !== null && 'msg' in item
              ? String((item as { msg: unknown }).msg)
              : '',
          )
          .filter((msg) => msg.length > 0)
        if (mensajes.length > 0) return mensajes.join(' · ')
      }
    }
  } catch {
    // Si la API no devuelve JSON, se utiliza el mensaje de respaldo.
  }

  return `${fallback} (${response.status})`
}

export const getCategorias = async (): Promise<Categoria[]> => {
  const response = await solicitar(`${API_URL}/`)
  if (!response.ok) {
    throw new Error(
      await obtenerMensajeError(response, 'No se pudieron cargar las categorías'),
    )
  }
  return response.json() as Promise<Categoria[]>
}

export const createCategoria = async (
  data: CategoriaInput,
): Promise<Categoria> => {
  const response = await solicitar(`${API_URL}/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    throw new Error(
      await obtenerMensajeError(response, 'No se pudo crear la categoría'),
    )
  }
  return response.json() as Promise<Categoria>
}

export const updateCategoria = async (
  categoriaId: number,
  data: CategoriaInput,
): Promise<Categoria> => {
  const response = await solicitar(`${API_URL}/${categoriaId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    throw new Error(
      await obtenerMensajeError(response, 'No se pudo editar la categoría'),
    )
  }
  return response.json() as Promise<Categoria>
}

export const deleteCategoria = async (categoriaId: number): Promise<void> => {
  const response = await solicitar(`${API_URL}/${categoriaId}`, {
    method: 'DELETE',
  })

  if (!response.ok) {
    throw new Error(
      await obtenerMensajeError(response, 'No se pudo eliminar la categoría'),
    )
  }
}
