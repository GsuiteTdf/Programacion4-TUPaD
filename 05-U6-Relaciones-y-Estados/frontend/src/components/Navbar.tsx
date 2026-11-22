export const Navbar = () => {
  return (
    <header className="bg-slate-950 text-white shadow-lg">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-widest text-blue-300">
            Food Store
          </p>
          <h1 className="text-xl font-bold tracking-tight">Gestor de Categorías</h1>
        </div>
        <span className="rounded-full bg-blue-400/10 px-3 py-1 text-sm font-medium text-blue-200">
          Unidad 6 · Full Stack
        </span>
      </nav>
    </header>
  )
}
