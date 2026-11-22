import type { Categoria } from '../types/categoria'
import { CategoriaCard } from './CategoriaCard'

interface CategoriaListProps {
  categorias: Categoria[]
  onEdit: (categoria: Categoria) => void
  onDelete: (categoria: Categoria) => void
}

export const CategoriaList = ({
  categorias,
  onEdit,
  onDelete,
}: CategoriaListProps) => {
  if (categorias.length === 0) {
    return (
      <div className="rounded-2xl border border-dashed border-slate-300 bg-white px-6 py-12 text-center">
        <p className="font-semibold text-slate-700">Todavía no hay categorías.</p>
        <p className="mt-1 text-sm text-slate-500">
          Usá el botón “Añadir categoría” para crear la primera.
        </p>
      </div>
    )
  }

  return (
    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      {categorias.map((categoria) => (
        <CategoriaCard
          key={categoria.id}
          categoria={categoria}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}
