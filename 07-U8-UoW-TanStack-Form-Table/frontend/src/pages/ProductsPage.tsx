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
import { LoadingState } from '../components/LoadingState'
import { ProductoList } from '../components/ProductoList'
import { ProductoModal } from '../components/ProductoModal'
import { createProducto, deleteProducto, getProductos, updateProducto } from '../services/producto'
import type { Producto, ProductoInput } from '../types/producto'
// keepDefaultValues: sin esta opción, reset() reemplaza los defaultValues y, en el siguiente render,
// useForm vuelve a aplicar los defaultValues vacíos: el modal de edición se abriría sin datos.
export function ProductsPage() {
  const qc = useQueryClient()
  const [open, setOpen] = useState(false)
  const [selected, setSelected] = useState<Producto | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [sorting, setSorting] = useState<SortingState>([])
  const q = useQuery({ queryKey: ['productos'], queryFn: getProductos })
  const refresh = () => qc.invalidateQueries({ queryKey: ['productos'] })
  const createM = useMutation({
    mutationFn: createProducto,
    onSuccess: async () => {
      await refresh()
      setOpen(false)
      setSelected(null)
    },
    onError: (e) => setError(e.message),
  })
  const updateM = useMutation({
    mutationFn: ({ id, data }: { id: number; data: ProductoInput }) => updateProducto(id, data),
    onSuccess: async () => {
      await refresh()
      setOpen(false)
      setSelected(null)
    },
    onError: (e) => setError(e.message),
  })
  const deleteM = useMutation({
    mutationFn: deleteProducto,
    onSuccess: refresh,
    onError: (e) => setError(e.message),
  })
  const form = useForm({
    defaultValues: { nombre: '', descripcion: '', precio_base: 0, imagenes: '', disponible: true },
    onSubmit: async ({ value }) => {
      const data: ProductoInput = {
        nombre: value.nombre,
        descripcion: value.descripcion,
        precio_base: Number(value.precio_base),
        imagenes_url: value.imagenes
          .split('\n')
          .map((v) => v.trim())
          .filter(Boolean),
        disponible: value.disponible,
      }
      setError(null)
      try {
        if (selected) await updateM.mutateAsync({ id: selected.id, data })
        else await createM.mutateAsync(data)
      } catch {
        /* onError muestra el error dentro del modal */
      }
    },
  })
  const openNew = () => {
    setSelected(null)
    setError(null)
    form.reset(
      { nombre: '', descripcion: '', precio_base: 0, imagenes: '', disponible: true },
      { keepDefaultValues: true },
    )
    setOpen(true)
  }
  const openEdit = (p: Producto) => {
    setSelected(p)
    setError(null)
    form.reset(
      {
        nombre: p.nombre,
        descripcion: p.descripcion,
        precio_base: p.precio_base,
        imagenes: p.imagenes_url.join('\n'),
        disponible: p.disponible,
      },
      { keepDefaultValues: true },
    )
    setOpen(true)
  }
  const remove = (p: Producto) => {
    setError(null)
    if (confirm(`¿Eliminar "${p.nombre}"?`)) deleteM.mutate(p.id)
  }
  const columns: ColumnDef<Producto>[] = [
    { accessorKey: 'nombre', header: 'Nombre' },
    { accessorKey: 'descripcion', header: 'Descripción' },
    {
      accessorKey: 'precio_base',
      header: 'Precio',
      cell: ({ row }) =>
        `$ ${row.original.precio_base.toLocaleString('es-AR', { minimumFractionDigits: 2 })}`,
    },
    {
      accessorKey: 'disponible',
      header: 'Disponible',
      cell: ({ row }) => (row.original.disponible ? 'Sí' : 'No'),
    },
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
          <h2 className="text-3xl font-bold">Productos</h2>
          <p className="text-slate-600">CRUD completo con TanStack</p>
        </div>
        <button
          onClick={openNew}
          className="rounded-lg bg-sky-700 px-4 py-2 font-semibold text-white"
        >
          Nuevo producto
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
        <EmptyState message="No hay productos cargados." />
      ) : (
        <ProductoList table={table} />
      )}
      <ProductoModal
        open={open}
        title={selected ? 'Editar producto' : 'Nuevo producto'}
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
        <form.Field name="descripcion">
          {(field) => (
            <label className="block text-sm font-semibold">
              Descripción
              <textarea
                className="mt-1 w-full rounded-lg border px-3 py-2"
                value={field.state.value}
                onChange={(e) => field.handleChange(e.target.value)}
              />
            </label>
          )}
        </form.Field>
        <form.Field
          name="precio_base"
          validators={{
            onChange: ({ value }) =>
              Number(value) < 0 ? 'El precio no puede ser negativo' : undefined,
          }}
        >
          {(field) => (
            <label className="block text-sm font-semibold">
              Precio base
              <input
                type="number"
                min="0"
                step="0.01"
                className="mt-1 w-full rounded-lg border px-3 py-2"
                value={field.state.value}
                onChange={(e) => field.handleChange(Number(e.target.value))}
              />
              {field.state.meta.errors.length > 0 && (
                <span className="text-sm text-red-700">{field.state.meta.errors.join(', ')}</span>
              )}
            </label>
          )}
        </form.Field>
        <form.Field name="imagenes">
          {(field) => (
            <label className="block text-sm font-semibold">
              Imágenes URL (una por línea)
              <textarea
                className="mt-1 w-full rounded-lg border px-3 py-2"
                value={field.state.value}
                onChange={(e) => field.handleChange(e.target.value)}
              />
            </label>
          )}
        </form.Field>
        <form.Field name="disponible">
          {(field) => (
            <label className="flex items-center gap-2 text-sm font-semibold">
              <input
                type="checkbox"
                checked={field.state.value}
                onChange={(e) => field.handleChange(e.target.checked)}
              />
              Disponible
            </label>
          )}
        </form.Field>
      </ProductoModal>
    </main>
  )
}
