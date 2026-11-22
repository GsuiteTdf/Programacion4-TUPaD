interface LoadingStateProps {
  message?: string
}
export function LoadingState({ message = 'Cargando datos…' }: LoadingStateProps) {
  return (
    <div className="rounded-xl border border-sky-200 bg-sky-50 p-5 text-sky-800">{message}</div>
  )
}
