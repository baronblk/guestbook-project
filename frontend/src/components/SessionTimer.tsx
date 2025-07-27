import React from 'react';
import { useSessionTimer } from '../hooks/useSessionTimer';
import { useAuthStore } from '../store/authStore';

interface SessionTimerProps {
  className?: string;
  showIcon?: boolean;
}

const SessionTimer: React.FC<SessionTimerProps> = ({ 
  className = '', 
  showIcon = true 
}) => {
  const { token } = useAuthStore();
  const { timeLeft, isExpiringSoon, isExpired, formatTimeLeft } = useSessionTimer();

  // Nicht anzeigen wenn nicht eingeloggt
  if (!token || timeLeft <= 0) {
    return null;
  }

  const getStatusColor = () => {
    if (isExpired) return 'text-red-600 bg-red-50 border-red-200';
    if (isExpiringSoon) return 'text-orange-600 bg-orange-50 border-orange-200';
    return 'text-green-600 bg-green-50 border-green-200';
  };

  const getStatusIcon = () => {
    if (isExpired) {
      return (
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
        </svg>
      );
    }
    if (isExpiringSoon) {
      return (
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
        </svg>
      );
    }
    return (
      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
      </svg>
    );
  };

  const getStatusText = () => {
    if (isExpired) return 'Session abgelaufen';
    if (isExpiringSoon) return 'Session läuft bald ab';
    return 'Session aktiv';
  };

  return (
    <div className={`inline-flex items-center gap-2 px-3 py-2 rounded-lg border text-sm font-medium transition-all duration-200 ${getStatusColor()} ${className}`}>
      {showIcon && getStatusIcon()}
      <div className="flex flex-col sm:flex-row sm:items-center sm:gap-2">
        <span className="hidden sm:inline">{getStatusText()}:</span>
        <span className="font-mono font-bold">
          {formatTimeLeft()}
        </span>
      </div>
    </div>
  );
};

export default SessionTimer;
