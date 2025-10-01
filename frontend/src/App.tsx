import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ToastProvider } from './context/ToastContext';
import { Suspense, lazy, useState } from 'react';
import ProtectedRoute from './components/common/ProtectedRoute';
import ErrorBoundary from './components/common/ErrorBoundary';
import Navbar from './components/layout/Navbar';
import Sidebar from './components/layout/Sidebar';
import './App.css';

// Lazy load pages
const Landing = lazy(() => import('./pages/Landing'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Login = lazy(() => import('./pages/Login'));
const Register = lazy(() => import('./pages/Register'));
const Transactions = lazy(() => import('./pages/Transactions'));
const Budgets = lazy(() => import('./pages/Budgets'));
const Reports = lazy(() => import('./pages/Reports'));
const Categories = lazy(() => import('./pages/Categories'));

const LoadingSpinner = () => (
  <div className="flex justify-center items-center h-64">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
  </div>
);

function App() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const DashboardLayout = ({ children }: { children: React.ReactNode }) => (
    <>
      <Navbar isMobileMenuOpen={isMobileMenuOpen} setIsMobileMenuOpen={setIsMobileMenuOpen} />
      <div className="flex">
        <Sidebar isMobileMenuOpen={isMobileMenuOpen} setIsMobileMenuOpen={setIsMobileMenuOpen} />
        <main className="flex-1 md:ml-64 p-4 md:p-6">
          {children}
        </main>
      </div>
    </>
  );

  return (
    <ErrorBoundary>
      <ToastProvider>
        <AuthProvider>
          <Router>
            <div className="min-h-screen bg-slate-50">
              <Suspense fallback={<LoadingSpinner />}>
                <Routes>
                  <Route path="/" element={<Landing />} />
                  <Route path="/login" element={<Login />} />
                  <Route path="/register" element={<Register />} />
                  <Route path="/dashboard" element={
                    <ProtectedRoute>
                      <DashboardLayout>
                        <Dashboard />
                      </DashboardLayout>
                    </ProtectedRoute>
                  } />
                  <Route path="/transactions" element={
                    <ProtectedRoute>
                      <DashboardLayout>
                        <Transactions />
                      </DashboardLayout>
                    </ProtectedRoute>
                  } />
                  <Route path="/categories" element={
                    <ProtectedRoute>
                      <DashboardLayout>
                        <Categories />
                      </DashboardLayout>
                    </ProtectedRoute>
                  } />
                  <Route path="/budgets" element={
                    <ProtectedRoute>
                      <DashboardLayout>
                        <Budgets />
                      </DashboardLayout>
                    </ProtectedRoute>
                  } />
                  <Route path="/reports" element={
                    <ProtectedRoute>
                      <DashboardLayout>
                        <Reports />
                      </DashboardLayout>
                    </ProtectedRoute>
                  } />
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
              </Suspense>
            </div>
          </Router>
        </AuthProvider>
      </ToastProvider>
    </ErrorBoundary>
  );
}

export default App;
