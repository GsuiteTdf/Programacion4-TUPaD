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
import { EmptyState } from '../components/EmptyState'
import { ErrorState } from '../components/ErrorState'
import { IngredienteList } from '../components/IngredienteList'
import { IngredienteModal } from '../components/IngredienteModal'
import { LoadingState } from '../components/LoadingState'
import {
  createIngrediente,
  deleteIngrediente,
  getIngredientes,
  updateIngrediente,
} from '../services/ingrediente'
import type { Ingrediente, IngredienteInput } from '../types/ingrediente'
// keepDefaultValues: sin esta opción, reset() reemplaza los defaultValues y, en el siguiente render,
// useForm vuelve a aplicar los defaultValues vacíos: el modal de edición se abriría sin datos.
export function IngredientesPage() {
  const qc = useQueryClient()
  const [open, setOpen] = useState(false)
  const [selected, setSelected] = useState<Ingrediente | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [sorting, setSorting] = useState<SortingState>([])
  const q = useQuery({ queryKey: ['ingredientes'], queryFn: getIngredientes })
  const refresh = () => qc.invalidateQueries({ queryKey: ['ingredientes'] })
  const createM = useMutation({
    mutationFn: createIngrediente,
    onSuccess: async () => {
      await refresh()
      setOpen(false)
      setSelected(null)
    },
    onError: (e) => setError(e.message),
  })
  const updateM = useMutation({
    mutationFn: ({ id, data }: { id: number; data: IngredienteInput }) =>
      updateIngrediente(id, data),
    onSuccess: async () => {
      await refresh()
      setOpen(false)
      setSelected(null)
    },
    onError: (e) => setError(e.message),
  })
  const deleteM = useMutation({
    mutationFn: deleteIngrediente,
    onSuccess: refresh,
    onError: (e) => setError(e.message),
  })
  const form = useForm({
    defaultValues: { nombre: '' },
    onSubmit: async ({ value }) => {
      setError(null)
      try {
        if (selected) await updateM.mutateAsync({ id: selected.id, data: value })
        else await createM.mutateAsync(value)
      } catch {
        /* onError muestra el error dentro del modal */
      }
    },
  })
  const openNew = () => {
    setSelected(null)
    setError(null)
    form.reset({ nombre: '' }, { keepDefaultValues: true })
    setOpen(true)
  }
  const openEdit = (i: Ingrediente) => {
    setSelected(i)
    setError(null)
    form.reset({ nombre: i.nombre }, { keepDefaultValues: true })
    setOpen(true)
  }
  const remove = (i: Ingrediente) => {
    setError(null)
    if (confirm(`¿Eliminar "${i.nombre}"?`)) deleteM.mutate(i.id)
  }
  const columns: ColumnDef<Ingrediente>[] = [
    { accessorKey: 'nombre', header: 'Nombre' },
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
    data: q.data ?? [],
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
      <div className="mb-6 flex justify-between">
        <div>
          <h2 className="text-3xl font-bold">Ingredientes</h2>
          <p className="text-slate-600">CRUD completo con TanStack</p>
        </div>
        <button
          onClick={openNew}
          className="rounded-lg bg-sky-700 px-4 py-2 font-semibold text-white"
        >
          Nuevo ingrediente
        </button>
      </div>
      {error && !open && (
        <div className="mb-4">
          <ErrorState message={error} />
        </div>
      )}
      {q.isPending ? (
        <LoadingState />
      ) : q.isError ? (
        <ErrorState message={q.error.message} onRetry={() => void q.refetch()} />
      ) : q.data.length === 0 ? (
        <EmptyState message="No hay ingredientes cargados." />
      ) : (
        <IngredienteList table={table} />
      )}
      <IngredienteModal
        open={open}
        title={selected ? 'Editar ingrediente' : 'Nuevo ingrediente'}
        error={error}
        saving={saving}
        onClose={() => {
          if (!saving) {
            setOpen(false)
            setSelected(null)
            setError(null)
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
                onChange={(e) => field.handleChange(e.target.value)}
              />
              {field.state.meta.errors.length > 0 && (
                <span className="text-sm text-red-700">{field.state.meta.errors.join(', ')}</span>
              )}
            </label>
          )}
        </form.Field>
      </IngredienteModal>
    </main>
  )
}
