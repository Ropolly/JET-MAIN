import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { MantineProvider } from '@mantine/core';
import './App.css';

// Context Providers
import { AuthProvider } from './contexts/AuthContext';
import { AppProvider } from './contexts/AppContext';
import { ThemeProvider } from './contexts/ThemeContext';

// Components
import { AppLayout } from './components/AppLayout';
import { ProtectedRoute } from './components/ProtectedRoute';

// Pages
import { HomePage } from './pages/HomePage';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { QuotesPage } from './pages/QuotesPage';
import { TripsPage } from './pages/TripsPage';

function App() {
  return (
    <MantineProvider>
      <ThemeProvider>
        <AuthProvider>
          <Router>
          <Routes>
            {/* Public routes */}
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            
            {/* Operations routes */}
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <AppProvider>
                  <AppLayout>
                    <DashboardPage />
                  </AppLayout>
                </AppProvider>
              </ProtectedRoute>
            } />
            
            <Route path="/quotes" element={
              <ProtectedRoute>
                <AppProvider>
                  <AppLayout>
                    <QuotesPage />
                  </AppLayout>
                </AppProvider>
              </ProtectedRoute>
            } />
            
            <Route path="/trips" element={
              <ProtectedRoute>
                <AppProvider>
                  <AppLayout>
                    <TripsPage />
                  </AppLayout>
                </AppProvider>
              </ProtectedRoute>
            } />

            <Route path="/patients" element={
              <ProtectedRoute>
                <AppProvider>
                  <AppLayout>
                    <DashboardPage />
                  </AppLayout>
                </AppProvider>
              </ProtectedRoute>
            } />
            
            {/* Admin routes */}
            <Route path="/admin/users" element={
              <ProtectedRoute>
                <AppProvider>
                  <AppLayout>
                    <DashboardPage />
                  </AppLayout>
                </AppProvider>
              </ProtectedRoute>
            } />
            
            <Route path="/admin/settings" element={
              <ProtectedRoute>
                <AppProvider>
                  <AppLayout>
                    <DashboardPage />
                  </AppLayout>
                </AppProvider>
              </ProtectedRoute>
            } />
            
            <Route path="/admin/reports" element={
              <ProtectedRoute>
                <AppProvider>
                  <AppLayout>
                    <DashboardPage />
                  </AppLayout>
                </AppProvider>
              </ProtectedRoute>
            } />
            
            {/* Maintenance routes */}
            <Route path="/maintenance/aircraft" element={
              <ProtectedRoute>
                <AppProvider>
                  <AppLayout>
                    <DashboardPage />
                  </AppLayout>
                </AppProvider>
              </ProtectedRoute>
            } />
            
            <Route path="/maintenance/equipment" element={
              <ProtectedRoute>
                <AppProvider>
                  <AppLayout>
                    <DashboardPage />
                  </AppLayout>
                </AppProvider>
              </ProtectedRoute>
            } />
            
            <Route path="/maintenance/schedules" element={
              <ProtectedRoute>
                <AppProvider>
                  <AppLayout>
                    <DashboardPage />
                  </AppLayout>
                </AppProvider>
              </ProtectedRoute>
            } />
            
            {/* Self routes */}
            <Route path="/profile" element={
              <ProtectedRoute>
                <AppProvider>
                  <AppLayout>
                    <DashboardPage />
                  </AppLayout>
                </AppProvider>
              </ProtectedRoute>
            } />
            
            <Route path="/preferences" element={
              <ProtectedRoute>
                <AppProvider>
                  <AppLayout>
                    <DashboardPage />
                  </AppLayout>
                </AppProvider>
              </ProtectedRoute>
            } />
            
            <Route path="/tasks" element={
              <ProtectedRoute>
                <AppProvider>
                  <AppLayout>
                    <DashboardPage />
                  </AppLayout>
                </AppProvider>
              </ProtectedRoute>
            } />
            
            {/* Fallback route */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
          </Router>
        </AuthProvider>
      </ThemeProvider>
    </MantineProvider>
  );
}

export default App;
