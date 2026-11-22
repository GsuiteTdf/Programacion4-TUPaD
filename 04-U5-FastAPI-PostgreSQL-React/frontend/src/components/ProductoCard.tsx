import type { Producto } from '../types/producto'

interface ProductoCardProps {
  producto: Producto
}

const formatearPrecio = (precio: number) =>
  new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    maximumFractionDigits: 2,
  }).format(precio)

export const ProductoCard = ({ producto }: ProductoCardProps) => {
  return (
    <article className="flex h-full flex-col justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition-shadow hover:shadow-md">
      <div>
        <div className="mb-4 flex items-start justify-between gap-4">
          <span className="rounded-lg bg-emerald-50 px-2.5 py-1 text-xs font-bold text-emerald-700">
            #{producto.id}
          </span>
          <span className="text-lg font-bold text-slate-900">
            {formatearPrecio(producto.precio)}
          </span>
        </div>
        <h2 className="text-xl font-bold tracking-tight text-slate-900">{producto.nombre}</h2>
        <p className="mt-2 text-sm leading-relaxed text-slate-600">{producto.descripcion}</p>
      </div>
      <button
        type="button"
        className="mt-6 w-full rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2"
      >
        Ver producto
      </button>
    </article>
  )
}
