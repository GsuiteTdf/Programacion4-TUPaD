interface EmptyStateProps {
  message: string
}
export function EmptyState({ message }: EmptyStateProps) {
  return (
    <div className="rounded-xl border border-dashed border-slate-300 bg-white p-8 text-center text-slate-500">
      {message}
    </div>
  )
}
