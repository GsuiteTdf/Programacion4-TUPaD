export interface UsuarioAuth {
  id: number
  nombre: string
  apellido: string
  email: string
  celular?: string | null
  roles: string[]
}
export interface LoginCredentials { email: string; password: string }
export interface RegisterInput { nombre: string; apellido: string; email: string; celular?: string; password: string }
export interface AdminUser extends UsuarioAuth { activo: boolean }
