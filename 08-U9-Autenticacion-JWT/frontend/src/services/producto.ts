import { apiErrorMessage, axiosInstance } from '../api/axiosInstance'
import type { Producto, ProductoInput } from '../types/producto'

export async function getProductos(): Promise<Producto[]> {
  try { return (await axiosInstance.get<Producto[]>('/productos/')).data }
  catch (error) { throw new Error(apiErrorMessage(error)) }
}

export async function createProducto(data: ProductoInput): Promise<Producto> {
  try { return (await axiosInstance.post<Producto>('/productos/', data)).data }
  catch (error) { throw new Error(apiErrorMessage(error)) }
}

export async function updateProducto(id: number, data: ProductoInput): Promise<Producto> {
  try { return (await axiosInstance.put<Producto>(`/productos/${id}`, data)).data }
  catch (error) { throw new Error(apiErrorMessage(error)) }
}

export async function deleteProducto(id: number): Promise<void> {
  try { await axiosInstance.delete(`/productos/${id}`) }
  catch (error) { throw new Error(apiErrorMessage(error)) }
}
