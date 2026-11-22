import type { Categoria } from '../types/categoria'

interface CategoriaCardProps {
  categoria: Categoria
  onEdit: (categoria: Categoria) => void
  onDelete: (categoria: Categoria) => void
}

export const CategoriaCard = ({
  categoria,
  onEdit,
  onDelete,
}: CategoriaCardProps) => {
  return (
    <article className="flex h-full flex-col justify-between rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-shadow hover:shadow-md">
      <div>
        <div className="mb-3 flex items-start justify-between gap-4">
          <span className="rounded-lg bg-blue-50 px-2.5 py-1 text-xs font-bold text-blue-700">
            #{categoria.id}
          </span>
          <span className="text-xs font-medium uppercase tracking-wide text-slate-400">
            Categoría
          </span>
        </div>
        <h2 className="text-xl font-bold tracking-tight text-slate-900">
          {categoria.nombre}
        </h2>
        <p className="mt-2 text-sm leading-relaxed text-slate-600">
          {categoria.descripcion || 'Sin descripción'}
        </p>
      </div>

      <div className="mt-6 flex gap-3">
        <button
          type="button"
          onClick={() => onEdit(categoria)}
          className="flex-1 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Editar
        </button>
        <button
          type="button"
          onClick={() => onDelete(categoria)}
          className="flex-1 rounded-lg border border-red-200 bg-red-50 px-4 py-2.5 text-sm font-semibold text-red-700 transition-colors hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
        >
          Eliminar
        </button>
      </div>
    </article>
  )
}
