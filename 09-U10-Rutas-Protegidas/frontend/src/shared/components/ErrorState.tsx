interface Props { message: string; onRetry?: () => void }
export function ErrorState({ message, onRetry }: Props) {
  return (
    <div className="rounded-xl border border-red-200 bg-red-50 p-5 text-red-800 dark:border-red-900 dark:bg-red-950/40 dark:text-red-200">
      <p>{message}</p>
      {onRetry && <button className="mt-3 rounded-lg border border-red-300 px-3 py-1.5 font-semibold dark:border-red-800" onClick={onRetry}>Reintentar</button>}
    </div>
  )
}
