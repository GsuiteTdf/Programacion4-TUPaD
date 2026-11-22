import type { Producto } from '../types/producto'
import { ProductoCard } from './ProductoCard'

interface ProductoListProps {
  productos: Producto[]
}

export const ProductoList = ({ productos }: ProductoListProps) => {
  return (
    <section aria-labelledby="productos-title">
      <div className="mb-6 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wide text-emerald-700">Catálogo</p>
          <h2 id="productos-title" className="text-2xl font-bold tracking-tight text-slate-900">
            Productos disponibles
          </h2>
        </div>
        <p className="text-sm text-slate-500">{productos.length} productos cargados</p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {productos.map((producto) => (
          <ProductoCard key={producto.id} producto={producto} />
        ))}
      </div>
    </section>
  )
}
