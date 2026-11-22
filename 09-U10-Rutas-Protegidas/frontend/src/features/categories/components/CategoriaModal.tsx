import type { FormEvent, ReactNode } from 'react'
interface Props { open: boolean; title: string; error: string | null; saving: boolean; onClose: () => void; onSubmit: (event: FormEvent<HTMLFormElement>) => void; children: ReactNode }
export function CategoriaModal({ open, title, error, saving, onClose, onSubmit, children }: Props) {
  if (!open) return null
  return <div className="fixed inset-0 z-50 grid place-items-center bg-slate-950/50 p-4"><div className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl dark:bg-slate-900"><h2 className="text-xl font-bold">{title}</h2><form onSubmit={onSubmit} className="mt-5 space-y-4">{children}{error && <div className="rounded-lg bg-red-50 p-3 text-sm text-red-800 dark:bg-red-950/40 dark:text-red-200">{error}</div>}<div className="flex justify-end gap-2"><button type="button" disabled={saving} onClick={onClose} className="rounded-lg border px-4 py-2 font-semibold dark:border-slate-700">Cancelar</button><button type="submit" disabled={saving} className="rounded-lg bg-sky-700 px-4 py-2 font-semibold text-white disabled:opacity-50">{saving ? 'Guardando…' : 'Guardar'}</button></div></form></div></div>
}
