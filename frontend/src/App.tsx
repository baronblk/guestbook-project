import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

// Components
import ReviewForm from './components/ReviewForm';
import ReviewList from './components/ReviewList';
import AdminLogin from './components/AdminLogin';
import AdminDashboard from './components/AdminDashboard';
import Layout from './components/Layout';

// Store
import { useAuthStore } from './store/authStore';

// Styles
import './index.css';

const App: React.FC = () => {
  const { checkAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  return (
    <Router>
      <div className="App">
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#10B981',
                secondary: '#fff',
              },
            },
            error: {
              duration: 5000,
              iconTheme: {
                primary: '#EF4444',
                secondary: '#fff',
              },
            },
          }}
        />

        <Routes>
          {/* Public Routes */}
          <Route
            path="/"
            element={
              <Layout>
                {/* Zentraler Container mit max-width 800px */}
                <div className="max-w-3xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
                  {/* Formular zur Bewertungsabgabe - zentriert oben */}
                  <div className="mb-12">
                    <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-200">
                      <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
                        Neue Bewertung abgeben
                      </h2>
                      <ReviewForm />
                    </div>
                  </div>

                  {/* Bewertungen - direkt darunter in derselben Breite */}
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">
                      Gästebuch-Einträge
                    </h2>
                    <ReviewList />
                  </div>
                </div>
              </Layout>
            }
          />

          {/* Admin Routes */}
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route
            path="/admin/*"
            element={
              <ProtectedRoute>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />

          {/* Embed Route */}
          <Route
            path="/embed"
            element={
              <div className="min-h-screen bg-gray-50 py-4">
                <div className="max-w-2xl mx-auto px-4">
                  <ReviewList embedded />
                </div>
              </div>
            }
          />

          {/* Redirect */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
};

// Protected Route Wrapper
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { token } = useAuthStore();

  if (!token) {
    return <Navigate to="/admin/login" replace />;
  }

  return <>{children}</>;
};

export default App;
