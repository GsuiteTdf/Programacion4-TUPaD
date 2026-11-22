import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { CategoriaList } from '../components/CategoriaList'
import { CategoriaModal } from '../components/CategoriaModal'
import {
  createCategoria,
  deleteCategoria,
  getCategorias,
  updateCategoria,
} from '../services/categoria'
import type { Categoria, CategoriaInput } from '../types/categoria'

export const CategoriasPage = () => {
  const queryClient = useQueryClient()
  const [modalAbierto, setModalAbierto] = useState(false)
  const [categoriaSeleccionada, setCategoriaSeleccionada] =
    useState<Categoria | null>(null)

  const categoriasQuery = useQuery({
    queryKey: ['categorias'],
    queryFn: getCategorias,
  })

  const createMutation = useMutation({
    mutationFn: createCategoria,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['categorias'] })
      cerrarModal()
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({
      categoriaId,
      data,
    }: {
      categoriaId: number
      data: CategoriaInput
    }) => updateCategoria(categoriaId, data),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['categorias'] })
      cerrarModal()
    },
  })

  const deleteMutation = useMutation({
    mutationFn: deleteCategoria,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['categorias'] })
    },
  })

  const abrirCrear = () => {
    createMutation.reset()
    updateMutation.reset()
    setCategoriaSeleccionada(null)
    setModalAbierto(true)
  }

  const abrirEditar = (categoria: Categoria) => {
    createMutation.reset()
    updateMutation.reset()
    setCategoriaSeleccionada(categoria)
    setModalAbierto(true)
  }

  const cerrarModal = () => {
    setModalAbierto(false)
    setCategoriaSeleccionada(null)
  }

  const guardarCategoria = (data: CategoriaInput) => {
    if (categoriaSeleccionada) {
      updateMutation.mutate({
        categoriaId: categoriaSeleccionada.id,
        data,
      })
      return
    }
    createMutation.mutate(data)
  }

  const eliminarCategoria = (categoria: Categoria) => {
    const confirmado = window.confirm(
      `¿Eliminar la categoría “${categoria.nombre}”?`,
    )
    if (!confirmado) return
    deleteMutation.mutate(categoria.id)
  }

  const errorModal = createMutation.error ?? updateMutation.error
  const errorPagina = categoriasQuery.error ?? deleteMutation.error

  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <section aria-labelledby="categorias-title">
        <div className="mb-7 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-blue-700">
              TanStack Query + FastAPI
            </p>
            <h1 id="categorias-title" className="text-3xl font-bold tracking-tight text-slate-900">
              Categorías
            </h1>
            <p className="mt-1 max-w-2xl text-sm text-slate-500">
              CRUD Full Stack con estado del servidor administrado por TanStack Query.
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

        {errorPagina && (
          <div role="alert" className="mb-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-800">
            {errorPagina instanceof Error ? errorPagina.message : 'Ocurrió un error inesperado.'}
          </div>
        )}

        {categoriasQuery.isPending ? (
          <div className="rounded-2xl border border-slate-200 bg-white px-6 py-12 text-center text-slate-500 shadow-sm">
            Cargando categorías…
          </div>
        ) : categoriasQuery.isError ? (
          <div className="rounded-2xl border border-slate-200 bg-white px-6 py-12 text-center shadow-sm">
            <p className="text-slate-600">No se pudo obtener el listado.</p>
            <button
              type="button"
              onClick={() => void categoriasQuery.refetch()}
              className="mt-4 rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700"
            >
              Reintentar
            </button>
          </div>
        ) : (
          <CategoriaList
            categorias={categoriasQuery.data}
            onEdit={abrirEditar}
            onDelete={eliminarCategoria}
            eliminandoId={
              deleteMutation.isPending ? (deleteMutation.variables ?? null) : null
            }
          />
        )}
      </section>

      {modalAbierto && (
        <CategoriaModal
          key={categoriaSeleccionada?.id ?? 'nueva'}
          abierto={modalAbierto}
          categoria={categoriaSeleccionada}
          guardando={createMutation.isPending || updateMutation.isPending}
          error={errorModal instanceof Error ? errorModal.message : null}
          onClose={cerrarModal}
          onSubmit={guardarCategoria}
        />
      )}
    </main>
  )
}
