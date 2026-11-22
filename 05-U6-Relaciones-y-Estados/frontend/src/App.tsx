import { useEffect, useState } from 'react'

import { CategoriaList } from './components/CategoriaList'
import { CategoriaModal } from './components/CategoriaModal'
import { Footer } from './components/Footer'
import { Navbar } from './components/Navbar'
import type { Categoria, CategoriaInput } from './types/categoria'

const API_URL = 'http://localhost:8000'

const obtenerMensajeError = async (response: Response, fallback: string) => {
  try {
    const data: unknown = await response.json()
    if (typeof data === 'object' && data !== null && 'detail' in data) {
      const detail = (data as { detail?: unknown }).detail

      if (typeof detail === 'string' && detail.trim().length > 0) {
        return detail
      }

      if (Array.isArray(detail)) {
        const mensajes = detail
          .map((item) => {
            if (typeof item === 'object' && item !== null && 'msg' in item) {
              const msg = (item as { msg?: unknown }).msg
              return typeof msg === 'string' ? msg : null
            }
            return null
          })
          .filter((mensaje): mensaje is string => mensaje !== null)

        if (mensajes.length > 0) {
          return mensajes.join('. ')
        }
      }
    }
  } catch {
    // Si la respuesta no contiene JSON válido, se usa el mensaje de respaldo.
  }

  return `${fallback} (${response.status})`
}

export const App = () => {
  const [categorias, setCategorias] = useState<Categoria[]>([])
  const [modalAbierto, setModalAbierto] = useState(false)
  const [categoriaSeleccionada, setCategoriaSeleccionada] =
    useState<Categoria | null>(null)
  const [cargando, setCargando] = useState(true)
  const [guardando, setGuardando] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const cargarCategorias = async () => {
    setCargando(true)
    setError(null)
    try {
      const response = await fetch(`${API_URL}/categorias/`)
      if (!response.ok) {
        throw new Error(
          await obtenerMensajeError(response, 'No se pudieron cargar las categorías'),
        )
      }
      const data: Categoria[] = await response.json()
      setCategorias(data)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Error inesperado al cargar categorías')
    } finally {
      setCargando(false)
    }
  }

  useEffect(() => {
    void cargarCategorias()
  }, [])

  const abrirCrear = () => {
    setCategoriaSeleccionada(null)
    setError(null)
    setModalAbierto(true)
  }

  const abrirEditar = (categoria: Categoria) => {
    setCategoriaSeleccionada(categoria)
    setError(null)
    setModalAbierto(true)
  }

  const cerrarModal = () => {
    if (guardando) return
    setModalAbierto(false)
    setCategoriaSeleccionada(null)
    setError(null)
  }

  const handleCreate = async (data: CategoriaInput) => {
    const response = await fetch(`${API_URL}/categorias/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!response.ok) {
      throw new Error(
        await obtenerMensajeError(response, 'No se pudo crear la categoría'),
      )
    }
    const creada: Categoria = await response.json()
    setCategorias((actuales) => [...actuales, creada])
  }

  const handleUpdate = async (categoriaId: number, data: CategoriaInput) => {
    const response = await fetch(`${API_URL}/categorias/${categoriaId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!response.ok) {
      throw new Error(
        await obtenerMensajeError(response, 'No se pudo editar la categoría'),
      )
    }
    const actualizada: Categoria = await response.json()
    setCategorias((actuales) =>
      actuales.map((categoria) =>
        categoria.id === actualizada.id ? actualizada : categoria,
      ),
    )
  }

  const guardarCategoria = async (data: CategoriaInput) => {
    setError(null)
    setGuardando(true)
    try {
      if (categoriaSeleccionada) {
        await handleUpdate(categoriaSeleccionada.id, data)
      } else {
        await handleCreate(data)
      }
      setModalAbierto(false)
      setCategoriaSeleccionada(null)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'No se pudo guardar la categoría')
      throw err
    } finally {
      setGuardando(false)
    }
  }

  const handleDelete = async (categoria: Categoria) => {
    const confirmado = window.confirm(
      `¿Eliminar la categoría “${categoria.nombre}”?`,
    )
    if (!confirmado) return

    setError(null)
    try {
      const response = await fetch(`${API_URL}/categorias/${categoria.id}`, {
        method: 'DELETE',
      })
      if (!response.ok) {
        throw new Error(
          await obtenerMensajeError(response, 'No se pudo eliminar la categoría'),
        )
      }
      setCategorias((actuales) =>
        actuales.filter((item) => item.id !== categoria.id),
      )
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'No se pudo eliminar la categoría')
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />

      <main className="mx-auto max-w-6xl px-6 py-10">
        <section aria-labelledby="categorias-title">
          <div className="mb-7 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-wide text-blue-700">
                CRUD Full Stack
              </p>
              <h2
                id="categorias-title"
                className="text-3xl font-bold tracking-tight text-slate-900"
              >
                Categorías
              </h2>
              <p className="mt-1 text-sm text-slate-500">
                Datos persistidos en FastAPI + SQLModel y consumidos con fetch nativo.
              </p>
            </div>

            <button
              type="button"
              onClick={abrirCrear}
              className="rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              + Añadir categoría
            </button>
          </div>

          {error && !modalAbierto && (
            <div
              role="alert"
              className="mb-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-800"
            >
              {error}
            </div>
          )}

          {cargando ? (
            <div className="rounded-2xl border border-slate-200 bg-white px-6 py-12 text-center text-slate-500 shadow-sm">
              Cargando categorías…
            </div>
          ) : (
            <CategoriaList
              categorias={categorias}
              onEdit={abrirEditar}
              onDelete={handleDelete}
            />
          )}
        </section>
      </main>

      <Footer />

      {modalAbierto && (
        <CategoriaModal
          key={categoriaSeleccionada?.id ?? 'nueva'}
          categoria={categoriaSeleccionada}
          error={error}
          guardando={guardando}
          onClose={cerrarModal}
          onSubmit={guardarCategoria}
        />
      )}
    </div>
  )
}
