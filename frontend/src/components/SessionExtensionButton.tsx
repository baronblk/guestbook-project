import React, { useState } from 'react';
import { useAuthStore } from '../store/authStore';
import { useSessionTimer } from '../hooks/useSessionTimer';
import toast from 'react-hot-toast';

interface SessionExtensionButtonProps {
  className?: string;
  autoShow?: boolean; // Automatisch anzeigen wenn Session bald abläuft
}

const SessionExtensionButton: React.FC<SessionExtensionButtonProps> = ({ 
  className = '',
  autoShow = true 
}) => {
  const [isExtending, setIsExtending] = useState(false);
  const { token, validateSession } = useAuthStore();
  const { isExpiringSoon } = useSessionTimer();

  // Nicht anzeigen wenn nicht eingeloggt oder nicht bald ablaufend (wenn autoShow aktiv)
  if (!token || (autoShow && !isExpiringSoon)) {
    return null;
  }

  const handleExtendSession = async () => {
    setIsExtending(true);
    try {
      // Session durch API-Call "verlängern" (Token wird automatisch refreshed wenn möglich)
      const isValid = await validateSession();
      if (isValid) {
        toast.success('Session wurde erfolgreich verlängert!', {
          duration: 3000,
          icon: '✅',
        });
      } else {
        toast.error('Session konnte nicht verlängert werden. Bitte melden Sie sich erneut an.');
      }
    } catch (error) {
      toast.error('Fehler beim Verlängern der Session.');
    } finally {
      setIsExtending(false);
    }
  };

  return (
    <button
      onClick={handleExtendSession}
      disabled={isExtending}
      className={`inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-orange-700 bg-orange-100 border border-orange-300 rounded-lg hover:bg-orange-200 focus:outline-none focus:ring-2 focus:ring-orange-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 ${className}`}
    >
      {isExtending ? (
        <>
          <div className="w-4 h-4 border-2 border-orange-600 border-t-transparent rounded-full animate-spin" />
          <span>Verlängere...</span>
        </>
      ) : (
        <>
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>Session verlängern</span>
        </>
      )}
    </button>
  );
};

export default SessionExtensionButton;
