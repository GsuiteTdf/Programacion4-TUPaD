import { apiErrorMessage, axiosInstance } from '../api/axiosInstance'
import type { AdminUser } from '../types/auth.types'

export async function getAdminUsers(): Promise<AdminUser[]> {
  try { return (await axiosInstance.get<AdminUser[]>('/api/v1/auth/admin/usuarios')).data }
  catch (error) { throw new Error(apiErrorMessage(error)) }
}

export async function setUserActive(id: number, active: boolean): Promise<AdminUser> {
  const action = active ? 'activar' : 'desactivar'
  try { return (await axiosInstance.post<AdminUser>(`/api/v1/auth/admin/usuarios/${id}/${action}`)).data }
  catch (error) { throw new Error(apiErrorMessage(error)) }
}
