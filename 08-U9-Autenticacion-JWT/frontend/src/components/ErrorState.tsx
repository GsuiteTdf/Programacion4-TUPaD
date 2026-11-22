interface ErrorStateProps {
  message: string
  onRetry?: () => void
}
export function ErrorState({ message, onRetry }: ErrorStateProps) {
  return (
    <div className="rounded-xl border border-red-200 bg-red-50 p-5 text-red-800">
      <p>{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-3 rounded-lg bg-red-700 px-3 py-2 text-sm font-semibold text-white"
        >
          Reintentar
        </button>
      )}
    </div>
  )
}
