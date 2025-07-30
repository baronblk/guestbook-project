import React from 'react';
import { AdminRole, AdminUser } from '../types';

interface RoleGuardProps {
  user: AdminUser;
  requiredRoles: AdminRole[];
  children: React.ReactNode;
  fallback?: React.ReactNode;
  showFallback?: boolean;
}

const RoleGuard: React.FC<RoleGuardProps> = ({
  user,
  requiredRoles,
  children,
  fallback,
  showFallback = true
}) => {
  const hasPermission = requiredRoles.includes(user.role);

  if (hasPermission) {
    return <>{children}</>;
  }

  if (showFallback && fallback) {
    return <>{fallback}</>;
  }

  if (showFallback) {
    return (
      <div className="text-center py-12">
        <div className="max-w-md mx-auto">
          <div className="text-6xl mb-4">🚫</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Zugriff verweigert
          </h3>
          <p className="text-sm text-gray-500 mb-4">
            Sie haben nicht die erforderlichen Berechtigungen für diese Funktion.
          </p>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex items-center space-x-2">
              <span className="text-yellow-600">⚠️</span>
              <span className="text-sm text-yellow-800">
                <strong>Erforderliche Berechtigung:</strong>{' '}
                {requiredRoles.map(role => {
                  switch (role) {
                    case AdminRole.MODERATOR:
                      return 'Moderator';
                    case AdminRole.ADMIN:
                      return 'Administrator';
                    case AdminRole.SUPERUSER:
                      return 'Super Admin';
                    default:
                      return role;
                  }
                }).join(' oder ')}
              </span>
            </div>
            <div className="flex items-center space-x-2 mt-2">
              <span className="text-yellow-600">👤</span>
              <span className="text-sm text-yellow-800">
                <strong>Ihre Berechtigung:</strong>{' '}
                {user.role === AdminRole.MODERATOR && 'Moderator'}
                {user.role === AdminRole.ADMIN && 'Administrator'}
                {user.role === AdminRole.SUPERUSER && 'Super Admin'}
              </span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return null;
};

// Helper Hooks für rollenbasierte Berechtigungen
export const useRolePermissions = (user: AdminUser | null) => {
  const hasRole = (requiredRoles: AdminRole[]): boolean => {
    if (!user) return false;
    return requiredRoles.includes(user.role);
  };

  const canModerate = (): boolean => {
    return hasRole([AdminRole.MODERATOR, AdminRole.ADMIN, AdminRole.SUPERUSER]);
  };

  const canManageUsers = (): boolean => {
    return hasRole([AdminRole.ADMIN, AdminRole.SUPERUSER]);
  };

  const canCreateSuperusers = (): boolean => {
    return hasRole([AdminRole.SUPERUSER]);
  };

  const canAccessImportExport = (): boolean => {
    return hasRole([AdminRole.MODERATOR, AdminRole.ADMIN, AdminRole.SUPERUSER]);
  };

  const canAccessSecurity = (): boolean => {
    return hasRole([AdminRole.SUPERUSER]);
  };

  const canAccessSystem = (): boolean => {
    return hasRole([AdminRole.SUPERUSER]);
  };

  return {
    hasRole,
    canModerate,
    canManageUsers,
    canCreateSuperusers,
    canAccessImportExport,
    canAccessSecurity,
    canAccessSystem
  };
};

export default RoleGuard;
