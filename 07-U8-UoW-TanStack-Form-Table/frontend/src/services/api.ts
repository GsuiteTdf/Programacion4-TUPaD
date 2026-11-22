export const API_URL = 'http://localhost:8000'

export async function apiError(response: Response): Promise<Error> {
  try {
    const body = (await response.json()) as { detail?: unknown }
    if (typeof body.detail === 'string') return new Error(body.detail)
    if (Array.isArray(body.detail)) {
      const messages = body.detail
        .map((item) => {
          if (typeof item === 'object' && item !== null && 'msg' in item) {
            return String((item as { msg: unknown }).msg)
          }
          return String(item)
        })
        .join('. ')
      return new Error(messages || `Error ${response.status}`)
    }
  } catch {
    // La API puede devolver una respuesta sin JSON.
  }
  return new Error(`La API respondió con error ${response.status}`)
}

export function networkError(error: unknown): Error {
  if (error instanceof TypeError) {
    return new Error('No se pudo conectar con el backend en localhost:8000')
  }
  return error instanceof Error ? error : new Error('Error inesperado')
}
