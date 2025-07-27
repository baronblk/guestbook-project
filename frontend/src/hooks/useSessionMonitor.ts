import { useEffect, useRef } from 'react';
import { useAuthStore } from '../store/authStore';
import toast from 'react-hot-toast';

export const useSessionMonitor = (intervalMinutes: number = 5) => {
  const { token, validateSession, logout } = useAuthStore();
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const warningShownRef = useRef<boolean>(false);

  useEffect(() => {
    // Nur überwachen wenn eingeloggt
    if (!token) {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
      warningShownRef.current = false;
      return;
    }

    // Session-Validierung alle X Minuten
    const validateSessionPeriodically = async () => {
      const isValid = await validateSession();
      
      if (!isValid) {
        toast.error('Session abgelaufen. Sie werden zur Anmeldung weitergeleitet...');
        return;
      }

      // Warnung wenn Session bald abläuft (basierend auf JWT-Token)
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const expiry = payload.exp * 1000; // JWT exp ist in Sekunden
        const now = Date.now();
        const timeLeft = expiry - now;
        const fiveMinutes = 5 * 60 * 1000;

        if (timeLeft <= fiveMinutes && timeLeft > 0 && !warningShownRef.current) {
          warningShownRef.current = true;
          toast('Ihre Session läuft in weniger als 5 Minuten ab!', {
            duration: 6000,
            icon: '⚠️',
            style: {
              background: '#FEF3C7',
              color: '#92400E',
              border: '1px solid #F59E0B',
            },
          });
        }

        // Reset warning flag wenn Session wieder länger gültig ist
        if (timeLeft > fiveMinutes) {
          warningShownRef.current = false;
        }
      } catch (error) {
        console.error('Error parsing token for session warning:', error);
      }
    };

    // Initiale Validierung
    validateSessionPeriodically();

    // Regelmäßige Validierung
    intervalRef.current = setInterval(
      validateSessionPeriodically,
      intervalMinutes * 60 * 1000
    );

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [token, validateSession, intervalMinutes]);

  // Auch bei Tab-Wechsel validieren
  useEffect(() => {
    if (!token) return;

    const handleVisibilityChange = () => {
      if (!document.hidden) {
        validateSession();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [token, validateSession]);
};
