import { useState } from 'react'
import { useForm } from '@tanstack/react-form'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  type ColumnDef,
  type SortingState,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from '@tanstack/react-table'
import { CategoriaList } from '../components/CategoriaList'
import { CategoriaModal } from '../components/CategoriaModal'
import { EmptyState } from '../components/EmptyState'
import { ErrorState } from '../components/ErrorState'
import { LoadingState } from '../components/LoadingState'
import {
  createCategoria,
  deleteCategoria,
  getCategorias,
  updateCategoria,
} from '../services/categoria'
import type { Categoria, CategoriaInput } from '../types/categoria'
// keepDefaultValues: sin esta opción, reset() reemplaza los defaultValues y, en el siguiente render,
// useForm vuelve a aplicar los defaultValues vacíos: el modal de edición se abriría sin datos.
export function CategoriasPage() {
  const qc = useQueryClient()
  const [modalOpen, setModalOpen] = useState(false)
  const [selected, setSelected] = useState<Categoria | null>(null)
  const [mutationError, setMutationError] = useState<string | null>(null)
  const [sorting, setSorting] = useState<SortingState>([])
  const query = useQuery({ queryKey: ['categorias'], queryFn: getCategorias })
  const refresh = () => qc.invalidateQueries({ queryKey: ['categorias'] })
  const createM = useMutation({
    mutationFn: createCategoria,
    onSuccess: async () => {
      await refresh()
      setModalOpen(false)
      setSelected(null)
    },
    onError: (e) => setMutationError(e.message),
  })
  const updateM = useMutation({
    mutationFn: ({ id, data }: { id: number; data: CategoriaInput }) => updateCategoria(id, data),
    onSuccess: async () => {
      await refresh()
      setModalOpen(false)
      setSelected(null)
    },
    onError: (e) => setMutationError(e.message),
  })
  const deleteM = useMutation({
    mutationFn: deleteCategoria,
    onSuccess: refresh,
    onError: (e) => setMutationError(e.message),
  })
  const form = useForm({
    defaultValues: { nombre: '', descripcion: '' },
    onSubmit: async ({ value }) => {
      setMutationError(null)
      try {
        if (selected) await updateM.mutateAsync({ id: selected.id, data: value })
        else await createM.mutateAsync(value)
      } catch {
        /* onError de la mutación mantiene el modal abierto y muestra el mensaje */
      }
    },
  })
  const openNew = () => {
    setSelected(null)
    setMutationError(null)
    form.reset({ nombre: '', descripcion: '' }, { keepDefaultValues: true })
    setModalOpen(true)
  }
  const openEdit = (c: Categoria) => {
    setSelected(c)
    setMutationError(null)
    form.reset({ nombre: c.nombre, descripcion: c.descripcion }, { keepDefaultValues: true })
    setModalOpen(true)
  }
  const remove = (c: Categoria) => {
    setMutationError(null)
    if (confirm(`¿Eliminar la categoría "${c.nombre}"?`)) deleteM.mutate(c.id)
  }
  const columns: ColumnDef<Categoria>[] = [
    { accessorKey: 'nombre', header: 'Nombre' },
    { accessorKey: 'descripcion', header: 'Descripción' },
    {
      id: 'acciones',
      header: 'Acciones',
      cell: ({ row }) => (
        <div className="flex gap-2">
          <button
            onClick={() => openEdit(row.original)}
            className="rounded bg-sky-700 px-3 py-1.5 text-sm font-semibold text-white"
          >
            Editar
          </button>
          <button
            disabled={deleteM.isPending && deleteM.variables === row.original.id}
            onClick={() => remove(row.original)}
            className="rounded bg-red-700 px-3 py-1.5 text-sm font-semibold text-white disabled:opacity-50"
          >
            Eliminar
          </button>
        </div>
      ),
    },
  ]
  const table = useReactTable({
    data: query.data ?? [],
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    initialState: { pagination: { pageSize: 5 } },
  })
  const saving = createM.isPending || updateM.isPending
  return (
    <main className="mx-auto max-w-6xl px-5 py-8">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold">Categorías</h2>
          <p className="text-slate-600">TanStack Query + Form + Table</p>
        </div>
        <button
          onClick={openNew}
          className="rounded-lg bg-sky-700 px-4 py-2 font-semibold text-white"
        >
          Nueva categoría
        </button>
      </div>
      {mutationError && !modalOpen && (
        <div className="mb-4">
          <ErrorState message={mutationError} />
        </div>
      )}
      {query.isPending ? (
        <LoadingState />
      ) : query.isError ? (
        <ErrorState message={query.error.message} onRetry={() => void query.refetch()} />
      ) : query.data.length === 0 ? (
        <EmptyState message="No hay categorías cargadas." />
      ) : (
        <CategoriaList table={table} />
      )}
      <CategoriaModal
        open={modalOpen}
        title={selected ? 'Editar categoría' : 'Nueva categoría'}
        error={mutationError}
        saving={saving}
        onClose={() => {
          if (!saving) {
            setModalOpen(false)
            setSelected(null)
            setMutationError(null)
          }
        }}
        onSubmit={(e) => {
          e.preventDefault()
          e.stopPropagation()
          void form.handleSubmit()
        }}
      >
        <form.Field
          name="nombre"
          validators={{
            onChange: ({ value }) => (value.trim() ? undefined : 'El nombre es obligatorio'),
          }}
        >
          {(field) => (
            <label className="block text-sm font-semibold">
              Nombre
              <input
                autoFocus
                className="mt-1 w-full rounded-lg border px-3 py-2"
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(e) => field.handleChange(e.target.value)}
              />
              {field.state.meta.errors.length > 0 && (
                <span className="text-sm text-red-700">{field.state.meta.errors.join(', ')}</span>
              )}
            </label>
          )}
        </form.Field>
        <form.Field name="descripcion">
          {(field) => (
            <label className="block text-sm font-semibold">
              Descripción
              <textarea
                className="mt-1 min-h-24 w-full rounded-lg border px-3 py-2"
                value={field.state.value}
                onChange={(e) => field.handleChange(e.target.value)}
              />
            </label>
          )}
        </form.Field>
      </CategoriaModal>
    </main>
  )
}
