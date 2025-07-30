import React from 'react';
import { AdminRole, AdminUser } from '../types';

interface RoleBasedNavigationProps {
  user: AdminUser;
  activeTab: string;
  onTabChange: (tab: string) => void;
}

interface NavTab {
  id: string;
  label: string;
  icon: string;
  requiredRoles: AdminRole[];
  description?: string;
}

const ALL_TABS: NavTab[] = [
  {
    id: 'moderation',
    label: 'Moderation',
    icon: '🛡️',
    requiredRoles: [AdminRole.MODERATOR, AdminRole.ADMIN, AdminRole.SUPERUSER],
    description: 'Bewertungen und Kommentare moderieren'
  },
  {
    id: 'reviews',
    label: 'Alle Bewertungen',
    icon: '⭐',
    requiredRoles: [AdminRole.MODERATOR, AdminRole.ADMIN, AdminRole.SUPERUSER],
    description: 'Übersicht aller Bewertungen'
  },
  {
    id: 'comments',
    label: 'Kommentare',
    icon: '💬',
    requiredRoles: [AdminRole.MODERATOR, AdminRole.ADMIN, AdminRole.SUPERUSER],
    description: 'Kommentar-Verwaltung'
  },
  {
    id: 'import-export',
    label: 'Import/Export',
    icon: '📁',
    requiredRoles: [AdminRole.MODERATOR, AdminRole.ADMIN, AdminRole.SUPERUSER],
    description: 'Daten importieren und exportieren'
  },
  {
    id: 'admin-management',
    label: 'Admin Verwaltung',
    icon: '👥',
    requiredRoles: [AdminRole.ADMIN, AdminRole.SUPERUSER],
    description: 'Benutzer verwalten'
  },
  {
    id: 'security',
    label: 'Sicherheit',
    icon: '🔒',
    requiredRoles: [AdminRole.SUPERUSER],
    description: 'Sicherheitseinstellungen'
  },
  {
    id: 'system',
    label: 'System',
    icon: '⚙️',
    requiredRoles: [AdminRole.SUPERUSER],
    description: 'Systemkonfiguration'
  }
];

const RoleBasedNavigation: React.FC<RoleBasedNavigationProps> = ({
  user,
  activeTab,
  onTabChange
}) => {
  // Filter tabs based on user role
  const availableTabs = ALL_TABS.filter(tab =>
    tab.requiredRoles.includes(user.role)
  );

  // Get role display information
  const getRoleInfo = (role: AdminRole) => {
    switch (role) {
      case AdminRole.MODERATOR:
        return { label: 'Moderator', color: 'text-blue-600', bgColor: 'bg-blue-100' };
      case AdminRole.ADMIN:
        return { label: 'Administrator', color: 'text-green-600', bgColor: 'bg-green-100' };
      case AdminRole.SUPERUSER:
        return { label: 'Super Admin', color: 'text-purple-600', bgColor: 'bg-purple-100' };
      default:
        return { label: 'Unbekannt', color: 'text-gray-600', bgColor: 'bg-gray-100' };
    }
  };

  const roleInfo = getRoleInfo(user.role);

  return (
    <div className="bg-white shadow-sm border-b">
      {/* User Role Header */}
      <div className="px-6 py-4 border-b bg-gray-50">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="text-lg font-semibold text-gray-900">
              Willkommen, {user.username}
            </div>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${roleInfo.color} ${roleInfo.bgColor}`}>
              {roleInfo.label}
            </span>
          </div>
          <div className="text-sm text-gray-500">
            Angemeldet seit: {new Date(user.last_login || user.created_at).toLocaleString('de-DE')}
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="px-6">
        <nav className="flex space-x-8 overflow-x-auto">
          {availableTabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`
                relative flex items-center space-x-2 py-4 px-2 border-b-2 font-medium text-sm whitespace-nowrap
                transition-colors duration-200
                ${activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }
              `}
              title={tab.description}
            >
              <span className="text-lg">{tab.icon}</span>
              <span>{tab.label}</span>
              {activeTab === tab.id && (
                <div className="absolute -bottom-0.5 left-0 right-0 h-0.5 bg-blue-500 rounded-full" />
              )}
            </button>
          ))}
        </nav>
      </div>

      {/* Role-based Information Bar */}
      <div className="px-6 py-2 bg-blue-50 text-sm text-blue-700">
        <div className="flex items-center space-x-4">
          <span className="font-medium">Verfügbare Funktionen:</span>
          <div className="flex items-center space-x-6">
            {user.role === AdminRole.MODERATOR && (
              <span>✓ Moderation, Bewertungen, Kommentare, Import/Export</span>
            )}
            {user.role === AdminRole.ADMIN && (
              <span>✓ Alle Moderator-Funktionen + Benutzerverwaltung</span>
            )}
            {user.role === AdminRole.SUPERUSER && (
              <span>✓ Vollzugriff auf alle Systemfunktionen</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RoleBasedNavigation;
