import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { adminApi } from '../api';
import { useAuthStore } from '../store/authStore';
import { AdminUser, AdminUserUpdate, PasswordChangeRequest } from '../types';
import Pagination from './Pagination';

interface AdminEditForm {
  username: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
}

interface PasswordChangeForm {
  old_password: string;
  new_password: string;
  new_password_confirm: string;
}

const AdminUserManagement: React.FC = () => {
  const { user: currentUser } = useAuthStore();
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedUser, setSelectedUser] = useState<AdminUser | null>(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalUsers, setTotalUsers] = useState(0);

  const {
    register: registerEdit,
    handleSubmit: handleEditSubmit,
    reset: resetEditForm,
    formState: { errors: editErrors }
  } = useForm<AdminEditForm>();

  const {
    register: registerPassword,
    handleSubmit: handlePasswordSubmit,
    reset: resetPasswordForm,
    watch,
    formState: { errors: passwordErrors }
  } = useForm<PasswordChangeForm>();

  const newPassword = watch('new_password');

  const loadUsers = async (page = 1) => {
    setLoading(true);
    try {
      const response = await adminApi.getAdminUsers({
        page,
        per_page: 10
      });
      setUsers(response.users);
      setTotalPages(response.total_pages);
      setTotalUsers(response.total);
      setCurrentPage(page);
    } catch (error) {
      toast.error('Fehler beim Laden der Admin-Benutzer');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleEditUser = (user: AdminUser) => {
    setSelectedUser(user);
    resetEditForm({
      username: user.username,
      email: user.email,
      is_active: user.is_active,
      is_superuser: user.is_superuser
    });
    setShowEditModal(true);
  };

  const handleUpdateUser = async (data: AdminEditForm) => {
    if (!selectedUser) return;

    try {
      const updateData: AdminUserUpdate = {
        username: data.username !== selectedUser.username ? data.username : undefined,
        email: data.email !== selectedUser.email ? data.email : undefined,
        is_active: data.is_active !== selectedUser.is_active ? data.is_active : undefined,
        is_superuser: data.is_superuser !== selectedUser.is_superuser ? data.is_superuser : undefined
      };

      await adminApi.updateAdminUser(selectedUser.id, updateData);
      toast.success('Admin-Benutzer erfolgreich aktualisiert');
      setShowEditModal(false);
      loadUsers(currentPage);
    } catch (error: any) {
      console.error('Admin update error:', error);
      const errorMessage = error.response?.data?.message || error.message || 'Fehler beim Aktualisieren des Admin-Benutzers';
      toast.error(errorMessage);
    }
  };

  const handleDeleteUser = async (user: AdminUser) => {
    if (user.id === currentUser?.id) {
      toast.error('Sie können sich nicht selbst löschen');
      return;
    }

    if (!window.confirm(`Admin-Benutzer "${user.username}" wirklich löschen?`)) {
      return;
    }

    try {
      await adminApi.deleteAdminUser(user.id);
      toast.success('Admin-Benutzer erfolgreich gelöscht');
      loadUsers(currentPage);
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || error.message || 'Fehler beim Löschen des Admin-Benutzers';
      toast.error(errorMessage);
    }
  };

  const handleToggleActive = async (user: AdminUser) => {
    if (user.id === currentUser?.id) {
      toast.error('Sie können sich nicht selbst deaktivieren');
      return;
    }

    try {
      if (user.is_active) {
        await adminApi.deactivateAdminUser(user.id);
        toast.success('Admin-Benutzer deaktiviert');
      } else {
        await adminApi.activateAdminUser(user.id);
        toast.success('Admin-Benutzer aktiviert');
      }
      loadUsers(currentPage);
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || error.message || 'Fehler beim Ändern des Status';
      toast.error(errorMessage);
    }
  };

  const handleChangePassword = async (data: PasswordChangeForm) => {
    try {
      const passwordData: PasswordChangeRequest = {
        old_password: data.old_password,
        new_password: data.new_password
      };

      await adminApi.changePassword(passwordData);
      toast.success('Passwort erfolgreich geändert');
      setShowPasswordModal(false);
      resetPasswordForm();
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || error.message || 'Fehler beim Ändern des Passworts. Prüfen Sie Ihr altes Passwort.';
      toast.error(errorMessage);
    }
  };

  const formatDate = (dateString: string | undefined | null) => {
    if (!dateString) return 'Nie';
    return new Date(dateString).toLocaleString('de-DE');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Admin-Benutzerverwaltung</h2>
        <button
          onClick={() => setShowPasswordModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Passwort ändern
        </button>
      </div>

      {/* User Table */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Admin-Benutzer ({totalUsers})
          </h3>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            Verwalten Sie Admin-Benutzer und ihre Berechtigungen
          </p>
        </div>

        {loading ? (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="mt-2 text-sm text-gray-500">Lade Admin-Benutzer...</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Benutzer
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Rollen
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Letzter Login
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Erstellt
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Aktionen
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {users.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="h-10 w-10 flex-shrink-0">
                          <div className="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                            <span className="text-sm font-medium text-gray-700">
                              {user.username.charAt(0).toUpperCase()}
                            </span>
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900 flex items-center">
                            {user.username}
                            {user.id === currentUser?.id && (
                              <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                Sie
                              </span>
                            )}
                          </div>
                          <div className="text-sm text-gray-500">{user.email}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        user.is_active
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {user.is_active ? 'Aktiv' : 'Inaktiv'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="space-y-1">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                          Admin
                        </span>
                        {user.is_superuser && (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                            Superuser
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatDate(user.last_login)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatDate(user.created_at)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                      <button
                        onClick={() => handleEditUser(user)}
                        className="text-indigo-600 hover:text-indigo-900"
                      >
                        Bearbeiten
                      </button>
                      {currentUser?.is_superuser && user.id !== currentUser.id && (
                        <>
                          <button
                            onClick={() => handleToggleActive(user)}
                            className={`${
                              user.is_active
                                ? 'text-red-600 hover:text-red-900'
                                : 'text-green-600 hover:text-green-900'
                            }`}
                          >
                            {user.is_active ? 'Deaktivieren' : 'Aktivieren'}
                          </button>
                          <button
                            onClick={() => handleDeleteUser(user)}
                            className="text-red-600 hover:text-red-900"
                          >
                            Löschen
                          </button>
                        </>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={(page) => loadUsers(page)}
        />
      )}

      {/* Edit User Modal */}
      {showEditModal && selectedUser && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-medium text-gray-900">
                  Admin-Benutzer bearbeiten
                </h3>
                <button
                  onClick={() => setShowEditModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <form onSubmit={handleEditSubmit(handleUpdateUser)} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Benutzername
                  </label>
                  <input
                    {...registerEdit('username', { required: 'Benutzername ist erforderlich' })}
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {editErrors.username && (
                    <p className="mt-1 text-sm text-red-600">{editErrors.username.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    E-Mail
                  </label>
                  <input
                    {...registerEdit('email', {
                      required: 'E-Mail ist erforderlich',
                      pattern: {
                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                        message: 'Ungültige E-Mail-Adresse'
                      }
                    })}
                    type="email"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {editErrors.email && (
                    <p className="mt-1 text-sm text-red-600">{editErrors.email.message}</p>
                  )}
                </div>

                <div className="flex items-center">
                  <input
                    {...registerEdit('is_active')}
                    type="checkbox"
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label className="ml-2 block text-sm text-gray-900">
                    Aktiv
                  </label>
                </div>

                {currentUser?.is_superuser && (
                  <div className="flex items-center">
                    <input
                      {...registerEdit('is_superuser')}
                      type="checkbox"
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label className="ml-2 block text-sm text-gray-900">
                      Superuser
                    </label>
                  </div>
                )}

                <div className="flex justify-end space-x-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowEditModal(false)}
                    className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
                  >
                    Abbrechen
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700"
                  >
                    Speichern
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Password Change Modal */}
      {showPasswordModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-medium text-gray-900">
                  Passwort ändern
                </h3>
                <button
                  onClick={() => setShowPasswordModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <form onSubmit={handlePasswordSubmit(handleChangePassword)} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Aktuelles Passwort
                  </label>
                  <input
                    {...registerPassword('old_password', { required: 'Aktuelles Passwort ist erforderlich' })}
                    type="password"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {passwordErrors.old_password && (
                    <p className="mt-1 text-sm text-red-600">{passwordErrors.old_password.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Neues Passwort
                  </label>
                  <input
                    {...registerPassword('new_password', {
                      required: 'Neues Passwort ist erforderlich',
                      minLength: {
                        value: 8,
                        message: 'Passwort muss mindestens 8 Zeichen lang sein'
                      }
                    })}
                    type="password"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {passwordErrors.new_password && (
                    <p className="mt-1 text-sm text-red-600">{passwordErrors.new_password.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Neues Passwort bestätigen
                  </label>
                  <input
                    {...registerPassword('new_password_confirm', {
                      required: 'Passwort-Bestätigung ist erforderlich',
                      validate: value => value === newPassword || 'Passwörter stimmen nicht überein'
                    })}
                    type="password"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {passwordErrors.new_password_confirm && (
                    <p className="mt-1 text-sm text-red-600">{passwordErrors.new_password_confirm.message}</p>
                  )}
                </div>

                <div className="flex justify-end space-x-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowPasswordModal(false)}
                    className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
                  >
                    Abbrechen
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700"
                  >
                    Passwort ändern
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminUserManagement;
