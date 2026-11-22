import { useState } from 'react'
import { useForm } from '@tanstack/react-form'
import { type ColumnDef, type SortingState, getCoreRowModel, getPaginationRowModel, getSortedRowModel, useReactTable } from '@tanstack/react-table'
import { apiErrorMessage } from '@/shared/api/api'
import { EmptyState } from '@/shared/components/EmptyState'
import { ErrorState } from '@/shared/components/ErrorState'
import { LoadingState } from '@/shared/components/LoadingState'
import { IngredienteList } from '../components/IngredienteList'
import { IngredienteModal } from '../components/IngredienteModal'
import { useIngredients } from '../hooks/useIngredients'
import type { Ingrediente } from '../types/ingredient.types'

export function IngredientsPage() {
  const { ingredients, isLoading, error: queryError, refetch, isAdmin, createIngredient, updateIngredient, deleteIngredient, isSaving, deletingId } = useIngredients()
  const [open, setOpen] = useState(false); const [selected, setSelected] = useState<Ingrediente | null>(null); const [formError, setFormError] = useState<string | null>(null); const [sorting, setSorting] = useState<SortingState>([])
  const form = useForm({ defaultValues: { nombre: '' }, onSubmit: async ({ value }) => { setFormError(null); try { if (selected) await updateIngredient(selected.id, value); else await createIngredient(value); setOpen(false); setSelected(null) } catch (e) { setFormError(apiErrorMessage(e)) } } })
  const openNew = () => { setSelected(null); setFormError(null); form.reset({ nombre: '' }, { keepDefaultValues: true }); setOpen(true) }
  const openEdit = (item: Ingrediente) => { setSelected(item); setFormError(null); form.reset({ nombre: item.nombre }, { keepDefaultValues: true }); setOpen(true) }
  const columns: ColumnDef<Ingrediente>[] = [{ accessorKey: 'nombre', header: 'Nombre' }, ...(isAdmin ? [{ id: 'acciones', header: 'Acciones', cell: ({ row }) => <div className="flex gap-2"><button onClick={() => openEdit(row.original)} className="rounded bg-sky-700 px-3 py-1.5 text-sm font-semibold text-white">Editar</button><button disabled={deletingId === row.original.id} onClick={() => { if (confirm(`¿Eliminar "${row.original.nombre}"?`)) void deleteIngredient(row.original.id) }} className="rounded bg-red-700 px-3 py-1.5 text-sm font-semibold text-white disabled:opacity-50">Eliminar</button></div> } as ColumnDef<Ingrediente>] : [])]
  const table = useReactTable({ data: ingredients, columns, state: { sorting }, onSortingChange: setSorting, getCoreRowModel: getCoreRowModel(), getSortedRowModel: getSortedRowModel(), getPaginationRowModel: getPaginationRowModel(), initialState: { pagination: { pageSize: 5 } } })
  return <main className="mx-auto max-w-6xl px-5 py-8"><div className="mb-6 flex justify-between"><div><h2 className="text-3xl font-bold">Ingredientes</h2><p className="text-slate-600 dark:text-slate-300">Arquitectura por features · useIngredients</p></div>{isAdmin && <button onClick={openNew} className="rounded-lg bg-sky-700 px-4 py-2 font-semibold text-white">Nuevo ingrediente</button>}</div>{isLoading ? <LoadingState /> : queryError ? <ErrorState message={queryError} onRetry={() => void refetch()} /> : ingredients.length === 0 ? <EmptyState message="No hay ingredientes cargados." /> : <IngredienteList table={table} />}<IngredienteModal open={open} title={selected ? 'Editar ingrediente' : 'Nuevo ingrediente'} error={formError} saving={isSaving} onClose={() => { if (!isSaving) { setOpen(false); setSelected(null); setFormError(null) } }} onSubmit={(e) => { e.preventDefault(); void form.handleSubmit() }}><form.Field name="nombre" validators={{ onChange: ({ value }) => value.trim() ? undefined : 'El nombre es obligatorio' }}>{(field) => <label className="block text-sm font-semibold">Nombre<input autoFocus className="mt-1 w-full rounded-lg border px-3 py-2 dark:border-slate-700 dark:bg-slate-950" value={field.state.value} onChange={(e) => field.handleChange(e.target.value)} />{field.state.meta.errors.length > 0 && <span className="text-sm text-red-700 dark:text-red-300">{field.state.meta.errors.join(', ')}</span>}</label>}</form.Field></IngredienteModal></main>
}
