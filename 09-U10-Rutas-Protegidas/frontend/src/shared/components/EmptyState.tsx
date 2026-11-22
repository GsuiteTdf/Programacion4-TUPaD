interface Props { message: string }
export function EmptyState({ message }: Props) {
  return <div className="rounded-xl border border-dashed bg-white p-8 text-center text-slate-500 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-400">{message}</div>
}
