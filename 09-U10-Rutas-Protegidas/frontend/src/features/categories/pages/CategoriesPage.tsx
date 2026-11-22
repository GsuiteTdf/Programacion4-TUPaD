import { useState } from 'react'
import { useForm } from '@tanstack/react-form'
import { type ColumnDef, type SortingState, getCoreRowModel, getPaginationRowModel, getSortedRowModel, useReactTable } from '@tanstack/react-table'
import { apiErrorMessage } from '@/shared/api/api'
import { EmptyState } from '@/shared/components/EmptyState'
import { ErrorState } from '@/shared/components/ErrorState'
import { LoadingState } from '@/shared/components/LoadingState'
import { CategoriaList } from '../components/CategoriaList'
import { CategoriaModal } from '../components/CategoriaModal'
import { useCategories } from '../hooks/useCategories'
import type { Categoria } from '../types/category.types'

export function CategoriesPage() {
  const { categories, isLoading, error: queryError, refetch, isAdmin, createCategory, updateCategory, deleteCategory, isSaving, deletingId } = useCategories()
  const [modalOpen, setModalOpen] = useState(false)
  const [selected, setSelected] = useState<Categoria | null>(null)
  const [formError, setFormError] = useState<string | null>(null)
  const [sorting, setSorting] = useState<SortingState>([])
  const form = useForm({ defaultValues: { nombre: '', descripcion: '' }, onSubmit: async ({ value }) => { setFormError(null); try { if (selected) await updateCategory(selected.id, value); else await createCategory(value); setModalOpen(false); setSelected(null) } catch (e) { setFormError(apiErrorMessage(e)) } } })
  const openNew = () => { setSelected(null); setFormError(null); form.reset({ nombre: '', descripcion: '' }, { keepDefaultValues: true }); setModalOpen(true) }
  const openEdit = (category: Categoria) => { setSelected(category); setFormError(null); form.reset({ nombre: category.nombre, descripcion: category.descripcion }, { keepDefaultValues: true }); setModalOpen(true) }
  const columns: ColumnDef<Categoria>[] = [
    { accessorKey: 'nombre', header: 'Nombre' },
    { accessorKey: 'descripcion', header: 'Descripción' },
    ...(isAdmin ? [{ id: 'acciones', header: 'Acciones', cell: ({ row }) => <div className="flex gap-2"><button onClick={() => openEdit(row.original)} className="rounded bg-sky-700 px-3 py-1.5 text-sm font-semibold text-white">Editar</button><button disabled={deletingId === row.original.id} onClick={() => { if (confirm(`¿Eliminar la categoría "${row.original.nombre}"?`)) void deleteCategory(row.original.id) }} className="rounded bg-red-700 px-3 py-1.5 text-sm font-semibold text-white disabled:opacity-50">Eliminar</button></div> } as ColumnDef<Categoria>] : []),
  ]
  const table = useReactTable({ data: categories, columns, state: { sorting }, onSortingChange: setSorting, getCoreRowModel: getCoreRowModel(), getSortedRowModel: getSortedRowModel(), getPaginationRowModel: getPaginationRowModel(), initialState: { pagination: { pageSize: 5 } } })
  return <main className="mx-auto max-w-6xl px-5 py-8"><div className="mb-6 flex items-center justify-between"><div><h2 className="text-3xl font-bold">Categorías</h2><p className="text-slate-600 dark:text-slate-300">Arquitectura por features · useCategories</p></div>{isAdmin && <button onClick={openNew} className="rounded-lg bg-sky-700 px-4 py-2 font-semibold text-white">Nueva categoría</button>}</div>{isLoading ? <LoadingState /> : queryError ? <ErrorState message={queryError} onRetry={() => void refetch()} /> : categories.length === 0 ? <EmptyState message="No hay categorías cargadas." /> : <CategoriaList table={table} />}<CategoriaModal open={modalOpen} title={selected ? 'Editar categoría' : 'Nueva categoría'} error={formError} saving={isSaving} onClose={() => { if (!isSaving) { setModalOpen(false); setSelected(null); setFormError(null) } }} onSubmit={(e) => { e.preventDefault(); void form.handleSubmit() }}><form.Field name="nombre" validators={{ onChange: ({ value }) => value.trim() ? undefined : 'El nombre es obligatorio' }}>{(field) => <label className="block text-sm font-semibold">Nombre<input autoFocus className="mt-1 w-full rounded-lg border px-3 py-2 dark:border-slate-700 dark:bg-slate-950" value={field.state.value} onBlur={field.handleBlur} onChange={(e) => field.handleChange(e.target.value)} />{field.state.meta.errors.length > 0 && <span className="text-sm text-red-700 dark:text-red-300">{field.state.meta.errors.join(', ')}</span>}</label>}</form.Field><form.Field name="descripcion">{(field) => <label className="block text-sm font-semibold">Descripción<textarea className="mt-1 min-h-24 w-full rounded-lg border px-3 py-2 dark:border-slate-700 dark:bg-slate-950" value={field.state.value} onChange={(e) => field.handleChange(e.target.value)} /></label>}</form.Field></CategoriaModal></main>
}
