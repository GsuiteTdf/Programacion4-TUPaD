import { flexRender, type Table } from '@tanstack/react-table'
import type { Categoria } from '../types/category.types'
export function CategoriaList({ table }: { table: Table<Categoria> }) {
  return (
    <div className="overflow-hidden rounded-xl border bg-white shadow-sm dark:border-slate-700 dark:bg-slate-900">
      <table className="min-w-full divide-y dark:divide-slate-700">
        <thead className="bg-slate-100 dark:bg-slate-800">{table.getHeaderGroups().map((group) => <tr key={group.id}>{group.headers.map((header) => <th key={header.id} className="px-4 py-3 text-left text-xs font-bold uppercase text-slate-600 dark:text-slate-300"><button onClick={header.column.getToggleSortingHandler()}>{flexRender(header.column.columnDef.header, header.getContext())}{{ asc: ' ↑', desc: ' ↓' }[header.column.getIsSorted() as string] ?? ''}</button></th>)}</tr>)}</thead>
        <tbody className="divide-y dark:divide-slate-700">{table.getRowModel().rows.map((row) => <tr key={row.id}>{row.getVisibleCells().map((cell) => <td key={cell.id} className="px-4 py-3 text-sm">{flexRender(cell.column.columnDef.cell, cell.getContext())}</td>)}</tr>)}</tbody>
      </table>
      <div className="flex justify-between border-t px-4 py-3 text-sm dark:border-slate-700"><span>Página {table.getState().pagination.pageIndex + 1} de {Math.max(table.getPageCount(), 1)}</span><div className="flex gap-2"><button disabled={!table.getCanPreviousPage()} onClick={() => table.previousPage()} className="rounded border px-3 py-1.5 disabled:opacity-40 dark:border-slate-700">Anterior</button><button disabled={!table.getCanNextPage()} onClick={() => table.nextPage()} className="rounded border px-3 py-1.5 disabled:opacity-40 dark:border-slate-700">Siguiente</button></div></div>
    </div>
  )
}
