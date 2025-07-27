import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuthStore } from '../store/authStore';

interface LoginForm {
  username: string;
  password: string;
}

const AdminLogin: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [sessionExpired, setSessionExpired] = useState(false);
  const { login, token } = useAuthStore();
  const navigate = useNavigate();
  
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<LoginForm>();

  // Check for session expiration message
  useEffect(() => {
    const expired = localStorage.getItem('session_expired');
    if (expired === 'true') {
      setSessionExpired(true);
      localStorage.removeItem('session_expired');
      toast.error('Ihre Session ist abgelaufen. Bitte melden Sie sich erneut an.');
    }
  }, []);

  // Redirect if already logged in
  useEffect(() => {
    if (token) {
      navigate('/admin', { replace: true });
    }
  }, [token, navigate]);

  const onSubmit = async (data: LoginForm) => {
    setIsLoading(true);
    try {
      const success = await login(data);
      if (success) {
        toast.success('Erfolgreich angemeldet!');
        // Navigate to admin dashboard after successful login
        navigate('/admin', { replace: true });
      }
    } catch (error) {
      toast.error('Anmeldung fehlgeschlagen. Bitte überprüfen Sie Ihre Daten.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Admin-Anmeldung
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Melden Sie sich an, um das Gästebuch zu verwalten
          </p>
        </div>

        {/* Session expired warning */}
        {sessionExpired && (
          <div className="rounded-md bg-yellow-50 p-4 border border-yellow-200">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-yellow-800">
                  Session abgelaufen
                </h3>
                <div className="mt-2 text-sm text-yellow-700">
                  <p>Ihre Anmeldesitzung ist abgelaufen. Bitte melden Sie sich erneut an, um fortzufahren.</p>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="username" className="sr-only">
                Benutzername
              </label>
              <input
                {...register('username', { required: 'Benutzername ist erforderlich' })}
                id="username"
                type="text"
                autoComplete="username"
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Benutzername"
              />
              {errors.username && (
                <p className="mt-1 text-sm text-red-600">{errors.username.message}</p>
              )}
            </div>
            
            <div>
              <label htmlFor="password" className="sr-only">
                Passwort
              </label>
              <input
                {...register('password', { required: 'Passwort ist erforderlich' })}
                id="password"
                type="password"
                autoComplete="current-password"
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Passwort"
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
              )}
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Anmelden...' : 'Anmelden'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AdminLogin;
