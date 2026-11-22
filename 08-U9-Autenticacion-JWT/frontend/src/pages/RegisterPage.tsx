import { useState } from 'react'
import { useForm } from '@tanstack/react-form'
import { useNavigate } from 'react-router-dom'
import { apiErrorMessage, axiosInstance } from '../api/axiosInstance'
import type { RegisterInput, UsuarioAuth } from '../types/auth.types'

export function RegisterPage() {
  const navigate = useNavigate()
  const [error, setError] = useState<string | null>(null)
  const form = useForm({
    defaultValues: { nombre: '', apellido: '', email: '', celular: '', password: '' },
    onSubmit: async ({ value }) => {
      setError(null)
      try {
        const payload: RegisterInput = { ...value, celular: value.celular.trim() || undefined }
        await axiosInstance.post<UsuarioAuth>('/api/v1/auth/register', payload)
        navigate('/login', { replace: true, state: { registered: true } })
      } catch (e) { setError(apiErrorMessage(e)) }
    },
  })
  return (
    <main className="mx-auto max-w-lg px-5 py-10">
      <h2 className="text-3xl font-bold">Crear cuenta</h2>
      <form className="mt-6 space-y-4 rounded-xl border bg-white p-6 shadow-sm" onSubmit={(e)=>{e.preventDefault(); void form.handleSubmit()}}>
        {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
        {(['nombre','apellido'] as const).map((name) => <form.Field key={name} name={name} validators={{onChange:({value})=>value.trim()?undefined:'Campo obligatorio'}}>{(field)=><label className="block text-sm font-semibold">{name === 'nombre' ? 'Nombre' : 'Apellido'}<input className="mt-1 w-full rounded-lg border px-3 py-2" value={field.state.value} onChange={(e)=>field.handleChange(e.target.value)} />{field.state.meta.errors.length>0 && <span className="text-sm text-red-700">{field.state.meta.errors.join(', ')}</span>}</label>}</form.Field>)}
        <form.Field name="email" validators={{onChange:({value})=>value.includes('@')?undefined:'Email inválido'}}>{(field)=><label className="block text-sm font-semibold">Email<input type="email" className="mt-1 w-full rounded-lg border px-3 py-2" value={field.state.value} onChange={(e)=>field.handleChange(e.target.value)} />{field.state.meta.errors.length>0 && <span className="text-sm text-red-700">{field.state.meta.errors.join(', ')}</span>}</label>}</form.Field>
        <form.Field name="celular">{(field)=><label className="block text-sm font-semibold">Celular (opcional)<input className="mt-1 w-full rounded-lg border px-3 py-2" value={field.state.value} onChange={(e)=>field.handleChange(e.target.value)} /></label>}</form.Field>
        <form.Field name="password" validators={{onChange:({value})=>value.length>=8?undefined:'Mínimo 8 caracteres'}}>{(field)=><label className="block text-sm font-semibold">Contraseña<input type="password" className="mt-1 w-full rounded-lg border px-3 py-2" value={field.state.value} onChange={(e)=>field.handleChange(e.target.value)} />{field.state.meta.errors.length>0 && <span className="text-sm text-red-700">{field.state.meta.errors.join(', ')}</span>}</label>}</form.Field>
        <button className="w-full rounded-lg bg-sky-700 px-4 py-2 font-semibold text-white" type="submit">Registrarme</button>
      </form>
    </main>
  )
}
