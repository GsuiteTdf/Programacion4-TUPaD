export interface Producto { id: number; nombre: string; descripcion: string; precio_base: number; imagenes_url: string[]; disponible: boolean; categorias: string[] }
export type ProductoInput = Omit<Producto, 'id' | 'categorias'>
