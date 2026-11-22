import type { Categoria } from '../types/categoria'
import { CategoriaCard } from './CategoriaCard'

interface CategoriaListProps {
  categorias: Categoria[]
  onEdit: (categoria: Categoria) => void
  onDelete: (categoria: Categoria) => void
  eliminandoId: number | null
}

export const CategoriaList = ({
  categorias,
  onEdit,
  onDelete,
  eliminandoId,
}: CategoriaListProps) => {
  if (categorias.length === 0) {
    return (
      <div className="rounded-2xl border border-dashed border-slate-300 bg-white px-6 py-12 text-center text-slate-500">
        No hay categorías registradas.
      </div>
    )
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {categorias.map((categoria) => (
        <CategoriaCard
          key={categoria.id}
          categoria={categoria}
          onEdit={onEdit}
          onDelete={onDelete}
          eliminando={eliminandoId === categoria.id}
        />
      ))}
    </div>
  )
}
