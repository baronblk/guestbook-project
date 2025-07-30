import { useCallback, useEffect, useState } from 'react';
import { useAuthStore } from '../store/authStore';

interface SessionTimerState {
  timeLeft: number; // Sekunden bis zum Ablauf
  isExpiringSoon: boolean; // Warnung wenn < 5 Minuten
  isExpired: boolean;
  formatTimeLeft: () => string;
}

export const useSessionTimer = (): SessionTimerState => {
  const { token } = useAuthStore();
  const [timeLeft, setTimeLeft] = useState<number>(0);
  const [sessionExpiry, setSessionExpiry] = useState<number | null>(null);

  // Token-Parsing um Ablaufzeit zu ermitteln
  const parseTokenExpiry = useCallback((token: string): number | null => {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp ? payload.exp * 1000 : null; // JWT exp ist in Sekunden, wir brauchen Millisekunden
    } catch (error) {
      console.error('Error parsing token:', error);
      return null;
    }
  }, []);

  // Session-Expiry berechnen wenn Token sich ändert
  useEffect(() => {
    if (token) {
      const expiry = parseTokenExpiry(token);
      setSessionExpiry(expiry);
    } else {
      setSessionExpiry(null);
      setTimeLeft(0);
    }
  }, [token, parseTokenExpiry]);

  // Timer-Update alle Sekunde
  useEffect(() => {
    if (!sessionExpiry) return;

    const updateTimer = () => {
      const now = Date.now();
      const remainingMs = sessionExpiry - now;
      const remainingSeconds = Math.max(0, Math.floor(remainingMs / 1000));
      setTimeLeft(remainingSeconds);
    };

    // Sofortiges Update
    updateTimer();

    // Intervall für Updates
    const interval = setInterval(updateTimer, 1000);

    return () => clearInterval(interval);
  }, [sessionExpiry]);

  // Zeit formatieren (MM:SS oder HH:MM:SS)
  const formatTimeLeft = useCallback((): string => {
    if (timeLeft <= 0) return '00:00';

    const hours = Math.floor(timeLeft / 3600);
    const minutes = Math.floor((timeLeft % 3600) / 60);
    const seconds = timeLeft % 60;

    if (hours > 0) {
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    } else {
      return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
  }, [timeLeft]);

  return {
    timeLeft,
    isExpiringSoon: timeLeft > 0 && timeLeft <= 600, // 10 Minuten Warnung
    isExpired: timeLeft <= 0 && sessionExpiry !== null,
    formatTimeLeft,
  };
};
