import { useCallback, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

export const useSessionManager = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { token, logout, refreshSession } = useAuthStore();

  // Session-Ablauf Behandlung
  const handleSessionExpired = useCallback(() => {
    logout();

    // Nur weiterleiten wenn wir im Admin-Bereich sind
    if (location.pathname.startsWith('/admin') && location.pathname !== '/admin/login') {
      // Session-Ablauf-Flag für Login-Seite setzen
      localStorage.setItem('session_expired', 'true');
      navigate('/admin/login', { replace: true });
    }
  }, [logout, navigate, location.pathname]);

  // Session-Überwachung
  useEffect(() => {
    // Prüfen ob Session-Ablauf-Flag gesetzt ist
    const sessionExpired = localStorage.getItem('session_expired');
    if (sessionExpired === 'true') {
      localStorage.removeItem('session_expired');
      handleSessionExpired();
      return;
    }

    // Nur im Admin-Bereich Session überwachen
    if (!token || !location.pathname.startsWith('/admin')) {
      return;
    }

    // Periodische Session-Validierung alle 5 Minuten
    const sessionCheckInterval = setInterval(async () => {
      try {
        // Versuche Session zu verlängern
        const refreshSuccess = await refreshSession();
        if (!refreshSuccess) {
          handleSessionExpired();
        }
      } catch (error) {
        console.error('Session validation failed:', error);
        handleSessionExpired();
      }
    }, 5 * 60 * 1000); // 5 Minuten

    // Cleanup
    return () => {
      clearInterval(sessionCheckInterval);
    };
  }, [token, location.pathname, refreshSession, handleSessionExpired]);

  // Event listener for unauthorized errors (global error handling)
  useEffect(() => {
    const handleUnauthorized = (event: CustomEvent) => {
      handleSessionExpired();
    };

    window.addEventListener('session-expired', handleUnauthorized as EventListener);

    return () => {
      window.removeEventListener('session-expired', handleUnauthorized as EventListener);
    };
  }, [handleSessionExpired]);
};
