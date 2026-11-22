import type { FormEvent } from 'react'

import { useForm } from '../hooks/useForm'
import type { Categoria, CategoriaInput } from '../types/categoria'

interface CategoriaModalProps {
  categoria: Categoria | null
  error: string | null
  guardando: boolean
  onClose: () => void
  onSubmit: (data: CategoriaInput) => Promise<void>
}

export const CategoriaModal = ({
  categoria,
  error,
  guardando,
  onClose,
  onSubmit,
}: CategoriaModalProps) => {
  const { values, updateField } = useForm<CategoriaInput>({
    nombre: categoria?.nombre ?? '',
    descripcion: categoria?.descripcion ?? '',
  })

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    try {
      await onSubmit(values)
    } catch {
      // App.tsx conserva y muestra el detalle del error; el modal permanece abierto.
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="categoria-modal-title"
    >
      <div className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl">
        <div className="mb-6">
          <p className="text-sm font-semibold uppercase tracking-wide text-blue-700">
            {categoria ? 'Edición' : 'Nuevo registro'}
          </p>
          <h2
            id="categoria-modal-title"
            className="text-2xl font-bold tracking-tight text-slate-900"
          >
            {categoria ? 'Editar categoría' : 'Añadir categoría'}
          </h2>
        </div>

        {error && (
          <div
            role="alert"
            className="mb-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-800"
          >
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="grid gap-4">
          <div className="flex flex-col gap-1">
            <label htmlFor="nombre" className="text-sm font-medium text-slate-700">
              Nombre
            </label>
            <input
              id="nombre"
              value={values.nombre}
              onChange={(event) => updateField('nombre', event.target.value)}
              required
              minLength={1}
              maxLength={120}
              autoFocus
              className="rounded-lg border border-slate-300 px-4 py-2.5 text-sm text-slate-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="flex flex-col gap-1">
            <label
              htmlFor="descripcion"
              className="text-sm font-medium text-slate-700"
            >
              Descripción
            </label>
            <textarea
              id="descripcion"
              value={values.descripcion}
              onChange={(event) => updateField('descripcion', event.target.value)}
              rows={4}
              maxLength={500}
              className="rounded-lg border border-slate-300 px-4 py-2.5 text-sm text-slate-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="mt-2 flex justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              disabled={guardando}
              className="rounded-lg border border-slate-300 px-5 py-2.5 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={guardando || values.nombre.trim().length === 0}
              className="rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {guardando ? 'Guardando…' : 'Guardar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
