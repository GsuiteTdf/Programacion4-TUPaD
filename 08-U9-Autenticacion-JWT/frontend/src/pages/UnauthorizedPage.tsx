import { Link } from 'react-router-dom'

export function UnauthorizedPage() {
  return <main className="mx-auto max-w-xl px-5 py-16 text-center"><h2 className="text-3xl font-bold">Acceso denegado</h2><p className="mt-3 text-slate-600">Tu usuario no tiene el rol necesario para acceder a esta sección.</p><Link className="mt-6 inline-block rounded-lg bg-sky-700 px-4 py-2 font-semibold text-white" to="/categories">Volver al catálogo</Link></main>
}
