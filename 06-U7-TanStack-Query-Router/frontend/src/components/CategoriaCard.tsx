import type { Categoria } from '../types/categoria'

interface CategoriaCardProps {
  categoria: Categoria
  onEdit: (categoria: Categoria) => void
  onDelete: (categoria: Categoria) => void
  eliminando: boolean
}

export const CategoriaCard = ({
  categoria,
  onEdit,
  onDelete,
  eliminando,
}: CategoriaCardProps) => (
  <article className="flex flex-col justify-between gap-5 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-shadow hover:shadow-md">
    <div>
      <p className="text-xs font-semibold uppercase tracking-wide text-blue-700">
        Categoría #{categoria.id}
      </p>
      <h3 className="mt-1 text-xl font-bold text-slate-900">{categoria.nombre}</h3>
      <p className="mt-2 text-sm leading-relaxed text-slate-600">
        {categoria.descripcion || 'Sin descripción.'}
      </p>
    </div>

    <div className="flex gap-2">
      <button
        type="button"
        onClick={() => onEdit(categoria)}
        className="flex-1 rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 transition-colors hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-400"
      >
        Editar
      </button>
      <button
        type="button"
        onClick={() => onDelete(categoria)}
        disabled={eliminando}
        className="flex-1 rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {eliminando ? 'Eliminando…' : 'Eliminar'}
      </button>
    </div>
  </article>
)
