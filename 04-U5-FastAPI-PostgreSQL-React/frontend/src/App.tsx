import { Footer } from './components/Footer'
import { Navbar } from './components/Navbar'
import { ProductoForm } from './components/ProductoForm'
import { ProductoList } from './components/ProductoList'
import type { Producto } from './types/producto'

const productos: Producto[] = [
  {
    id: 1,
    nombre: 'Café molido',
    descripcion: 'Café de tueste medio en paquete de 500 gramos.',
    precio: 8500,
  },
  {
    id: 2,
    nombre: 'Té verde',
    descripcion: 'Caja con 20 saquitos de té verde seleccionado.',
    precio: 4200,
  },
  {
    id: 3,
    nombre: 'Galletas artesanales',
    descripcion: 'Galletas de manteca elaboradas de manera artesanal.',
    precio: 5600,
  },
]

export const App = () => {
  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <main className="mx-auto grid max-w-6xl gap-10 px-6 py-10">
        <ProductoList productos={productos} />
        <ProductoForm />
      </main>
      <Footer />
    </div>
  )
}
