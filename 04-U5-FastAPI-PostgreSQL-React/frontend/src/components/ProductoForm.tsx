export const ProductoForm = () => {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm" aria-labelledby="form-title">
      <div className="mb-6">
        <p className="text-sm font-semibold uppercase tracking-wide text-emerald-700">Nuevo registro</p>
        <h2 id="form-title" className="text-2xl font-bold tracking-tight text-slate-900">
          Alta de producto
        </h2>
        <p className="mt-1 text-sm text-slate-500">
          Maquetado sin funcionalidad, según el alcance de la Unidad 5.
        </p>
      </div>

      <form className="grid gap-4 md:grid-cols-2">
        <div className="flex flex-col gap-1 md:col-span-2">
          <label htmlFor="nombre" className="text-sm font-medium text-slate-700">Nombre</label>
          <input
            id="nombre"
            name="nombre"
            type="text"
            placeholder="Ej. Café molido"
            className="rounded-lg border border-slate-300 px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
        </div>

        <div className="flex flex-col gap-1 md:col-span-2">
          <label htmlFor="descripcion" className="text-sm font-medium text-slate-700">Descripción</label>
          <textarea
            id="descripcion"
            name="descripcion"
            rows={3}
            placeholder="Descripción breve del producto"
            className="rounded-lg border border-slate-300 px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
        </div>

        <div className="flex flex-col gap-1">
          <label htmlFor="precio" className="text-sm font-medium text-slate-700">Precio</label>
          <input
            id="precio"
            name="precio"
            type="number"
            min="0"
            step="0.01"
            placeholder="0.00"
            className="rounded-lg border border-slate-300 px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
        </div>

        <div className="flex items-end gap-3">
          <button
            type="button"
            className="w-full rounded-lg bg-emerald-600 px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2"
          >
            Agregar
          </button>
          <button
            type="reset"
            className="w-full rounded-lg border border-slate-300 px-5 py-2.5 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-400"
          >
            Limpiar
          </button>
        </div>
      </form>
    </section>
  )
}
