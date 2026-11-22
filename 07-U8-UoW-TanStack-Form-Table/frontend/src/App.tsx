import { Route, Routes } from 'react-router-dom'
import { Navbar } from './components/Navbar'
import { CategoriasPage } from './pages/CategoriasPage'
import { IngredientesPage } from './pages/IngredientesPage'
import { ProductsPage } from './pages/ProductsPage'

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<CategoriasPage />} />
        <Route path="/categorias" element={<CategoriasPage />} />
        <Route path="/categories" element={<CategoriasPage />} />
        <Route path="/productos" element={<ProductsPage />} />
        <Route path="/products" element={<ProductsPage />} />
        <Route path="/ingredientes" element={<IngredientesPage />} />
        <Route path="/ingredients" element={<IngredientesPage />} />
      </Routes>
    </>
  )
}
