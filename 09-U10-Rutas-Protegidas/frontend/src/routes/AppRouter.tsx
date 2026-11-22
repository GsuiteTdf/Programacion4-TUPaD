import { Navigate, Route, Routes } from 'react-router-dom'
import { AdminUsersPage, LoginPage, RegisterPage } from '@/features/auth'
import { CategoriesPage } from '@/features/categories'
import { IngredientsPage } from '@/features/ingredients'
import { ProductsPage } from '@/features/products'
import { Navbar } from '@/shared/components/Navbar'
import { UnauthorizedPage } from '@/shared/components/UnauthorizedPage'
import { ProtectedRoute } from './ProtectedRoute'

export function AppRouter() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/categories" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/unauthorized" element={<UnauthorizedPage />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/categories" element={<CategoriesPage />} />
          <Route path="/products" element={<ProductsPage />} />
          <Route path="/ingredients" element={<IngredientsPage />} />
          <Route path="/categorias" element={<Navigate to="/categories" replace />} />
          <Route path="/productos" element={<Navigate to="/products" replace />} />
          <Route path="/ingredientes" element={<Navigate to="/ingredients" replace />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
          <Route path="/admin/users" element={<AdminUsersPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  )
}
