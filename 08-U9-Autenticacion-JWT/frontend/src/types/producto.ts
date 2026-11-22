export interface Producto {
  id: number
  nombre: string
  descripcion: string
  precio_base: number
  imagenes_url: string[]
  disponible: boolean
  // Nombres de las categorías del producto, calculados por el backend (solo lectura).
  categorias: string[]
}

export type ProductoInput = Omit<Producto, 'id' | 'categorias'>
