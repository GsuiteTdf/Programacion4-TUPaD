import { useState } from 'react'
import { useForm } from '@tanstack/react-form'
import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import { apiErrorMessage } from '../api/axiosInstance'
import { useAuthStore } from '../store/authStore'

export function LoginPage() {
  const user = useAuthStore((s) => s.user)
  const login = useAuthStore((s) => s.login)
  const navigate = useNavigate()
  const location = useLocation()
  const [error, setError] = useState<string | null>(null)
  const form = useForm({
    defaultValues: { email: '', password: '' },
    onSubmit: async ({ value }) => {
      setError(null)
      try {
        await login(value.email, value.password)
        const target = (location.state as { from?: string } | null)?.from ?? '/categories'
        navigate(target, { replace: true })
      } catch (e) { setError(apiErrorMessage(e)) }
    },
  })
  if (user) return <Navigate to="/categories" replace />
  return (
    <main className="mx-auto max-w-md px-5 py-12">
      <h2 className="text-3xl font-bold">Iniciar sesión</h2>
      <p className="mt-1 text-slate-600">El JWT viaja únicamente en una cookie HttpOnly.</p>
      <form className="mt-6 space-y-4 rounded-xl border bg-white p-6 shadow-sm" onSubmit={(e) => { e.preventDefault(); void form.handleSubmit() }}>
        {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
        <form.Field name="email" validators={{ onChange: ({value}) => value.includes('@') ? undefined : 'Ingrese un email válido' }}>
          {(field) => <label className="block text-sm font-semibold">Email<input type="email" className="mt-1 w-full rounded-lg border px-3 py-2" value={field.state.value} onChange={(e)=>field.handleChange(e.target.value)} />{field.state.meta.errors.length>0 && <span className="text-sm text-red-700">{field.state.meta.errors.join(', ')}</span>}</label>}
        </form.Field>
        <form.Field name="password" validators={{ onChange: ({value}) => value.length >= 8 ? undefined : 'La contraseña debe tener al menos 8 caracteres' }}>
          {(field) => <label className="block text-sm font-semibold">Contraseña<input type="password" className="mt-1 w-full rounded-lg border px-3 py-2" value={field.state.value} onChange={(e)=>field.handleChange(e.target.value)} />{field.state.meta.errors.length>0 && <span className="text-sm text-red-700">{field.state.meta.errors.join(', ')}</span>}</label>}
        </form.Field>
        <button className="w-full rounded-lg bg-sky-700 px-4 py-2 font-semibold text-white" type="submit">Ingresar</button>
      </form>
    </main>
  )
}
