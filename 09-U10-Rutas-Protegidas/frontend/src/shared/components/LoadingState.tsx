interface Props { message?: string }
export function LoadingState({ message = 'Cargando…' }: Props) {
  return <div className="rounded-xl border bg-white p-6 text-slate-600 shadow-sm dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300">{message}</div>
}
