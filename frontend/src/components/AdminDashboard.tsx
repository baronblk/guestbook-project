import React, { useCallback, useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import { adminApi } from '../api';
import { useSessionMonitor } from '../hooks/useSessionMonitor';
import { useAuthStore } from '../store/authStore';
import { useReviewStore } from '../store/reviewStore';
import { FullImportData } from '../types';
import AdminCommentsPanel from './AdminCommentsPanel';
import ImageModal from './ImageModal';
import ModerationPanel from './ModerationPanel';
import Pagination from './Pagination';
import RatingStars from './RatingStars';
import SessionExtensionButton from './SessionExtensionButton';
import SessionTimer from './SessionTimer';

interface CreateAdminForm {
  username: string;
  password: string;
  email: string;
}

const AdminDashboard: React.FC = () => {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const {
    reviews,
    filter,
    setFilter,
    fetchReviews,
    deleteReview,
    toggleReviewVisibility
  } = useReviewStore();

  // Session-Monitoring aktivieren (alle 3 Minuten)
  useSessionMonitor(3);

  const [activeTab, setActiveTab] = useState<'reviews' | 'moderation' | 'comments' | 'admin' | 'export'>('moderation');
  const [reviewFilter, setReviewFilter] = useState<'all' | 'approved' | 'hidden'>('all');
  const [isLoading, setIsLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalReviews, setTotalReviews] = useState(0);
  const [modalImage, setModalImage] = useState<string | null>(null);

  const {
    register: registerAdmin,
    handleSubmit: handleAdminSubmit,
    reset: resetAdminForm,
    formState: { errors: adminErrors }
  } = useForm<CreateAdminForm>();

  const loadReviews = useCallback(async () => {
    setIsLoading(true);
    try {
      // Admin-API verwenden mit entsprechendem Filter
      let approved_only: boolean | undefined;

      switch (reviewFilter) {
        case 'approved':
          approved_only = true;
          break;
        case 'hidden':
          approved_only = false;
          break;
        default:
          approved_only = undefined; // Alle anzeigen
      }

      const response = await adminApi.getReviews({
        page: currentPage,
        per_page: 10,
        approved_only
      });

      // Lokaler State aktualisieren
      reviews.splice(0, reviews.length, ...response.reviews);

      setTotalPages(Math.ceil(response.total / 10));
      setTotalReviews(response.total);
    } catch (error: any) {
      // Bessere Fehlerbehandlung für verschiedene HTTP-Status-Codes
      if (error.response?.status === 401 || error.response?.status === 403) {
        toast.error('Session abgelaufen. Sie werden zur Anmeldung weitergeleitet...');
        // Der Interceptor wird automatisch weiterleiten
      } else {
        toast.error('Fehler beim Laden der Bewertungen');
        console.error('Admin reviews fetch error:', error);
      }
    } finally {
      setIsLoading(false);
    }
  }, [currentPage, reviewFilter, reviews]);

  useEffect(() => {
    loadReviews();
  }, [loadReviews]); // loadReviews wird innerhalb des useEffect verwendet

  const handleDeleteReview = async (id: number) => {
    if (!window.confirm('Sind Sie sicher, dass Sie diese Bewertung löschen möchten?')) {
      return;
    }

    try {
      await deleteReview(id);
      toast.success('Bewertung gelöscht');
      loadReviews();
    } catch (error) {
      toast.error('Fehler beim Löschen der Bewertung');
    }
  };

  const handleToggleVisibility = async (id: number) => {
    try {
      await toggleReviewVisibility(id);
      toast.success('Sichtbarkeit geändert');
      loadReviews();
    } catch (error) {
      toast.error('Fehler beim Ändern der Sichtbarkeit');
    }
  };

  const handleCreateAdmin = async (data: CreateAdminForm) => {
    try {
      await adminApi.createAdmin(data);
      toast.success('Admin-Benutzer erstellt');
      resetAdminForm();
    } catch (error) {
      toast.error('Fehler beim Erstellen des Admin-Benutzers');
    }
  };

  const handleExportData = async () => {
    try {
      const data = await adminApi.exportFullData();
      const blob = new Blob([JSON.stringify(data, null, 2)], {
        type: 'application/json'
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `guestbook-full-export-${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      toast.success(`Vollständiger Export erstellt: ${data.total_reviews} Reviews, ${data.total_comments} Kommentare`);
    } catch (error) {
      toast.error('Fehler beim Exportieren der Daten');
    }
  };

  const handleImportData = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      const text = await file.text();
      const data: FullImportData = JSON.parse(text);

      // Warnung vor kompletter Datenwiederherstellung
      const confirmReplace = window.confirm(
        'Möchten Sie alle bestehenden Daten ersetzen? Diese Aktion kann nicht rückgängig gemacht werden!'
      );

      const result = await adminApi.importFullData(data, confirmReplace);

      if (result.errors.length > 0) {
        toast.error(`Import mit Fehlern: ${result.errors.length} Fehler aufgetreten`);
        console.error('Import errors:', result.errors);
      } else {
        toast.success(`Import erfolgreich: ${result.imported_reviews} Reviews, ${result.imported_comments} Kommentare`);
      }

      loadReviews(); // Daten neu laden
    } catch (error) {
      toast.error('Fehler beim Importieren der Daten - Überprüfen Sie das Dateiformat');
    }

    // Reset file input
    event.target.value = '';
  };

  const renderReviewsTab = () => (
    <div className="space-y-6">
      {/* Filters */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-medium mb-4">Filter</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              value={reviewFilter}
              onChange={(e) => {
                setReviewFilter(e.target.value as 'all' | 'approved' | 'hidden');
                setCurrentPage(1); // Zurück zur ersten Seite
              }}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">Alle Bewertungen</option>
              <option value="approved">Nur genehmigte</option>
              <option value="hidden">Nur versteckte</option>
            </select>
          </div>

        </div>
      </div>

      {/* Reviews List */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg font-medium mb-4">
            Bewertungen ({reviews.length} von {totalReviews})
          </h3>

          {isLoading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-2 text-gray-600">Lade Bewertungen...</p>
            </div>
          ) : reviews.length === 0 ? (
            <p className="text-center py-8 text-gray-500">Keine Bewertungen gefunden.</p>
          ) : (
            <div className="space-y-4">
              {reviews.map((review) => (
                <div key={review.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h4 className="font-semibold text-gray-900">{review.name}</h4>
                      <div className="flex items-center space-x-2 text-sm text-gray-500">
                        <RatingStars rating={review.rating} readonly />
                        <span>•</span>
                        <span>{new Date(review.created_at).toLocaleDateString('de-DE')}</span>
                        <span>•</span>
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          review.is_approved
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {review.is_approved ? 'Sichtbar' : 'Versteckt'}
                        </span>
                      </div>
                    </div>

                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleToggleVisibility(review.id)}
                        className={`px-3 py-1 text-xs rounded-md ${
                          review.is_approved
                            ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
                            : 'bg-green-100 text-green-800 hover:bg-green-200'
                        }`}
                      >
                        {review.is_approved ? 'Verstecken' : 'Anzeigen'}
                      </button>

                      <button
                        onClick={() => handleDeleteReview(review.id)}
                        className="px-3 py-1 text-xs bg-red-100 text-red-800 hover:bg-red-200 rounded-md"
                      >
                        Löschen
                      </button>
                    </div>
                  </div>

                  {review.content && (
                    <p className="text-gray-700 mb-2">{review.content}</p>
                  )}

                  {review.image_path && (
                    <div className="mt-2">
                      <img
                        src={`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}${review.image_path}`}
                        alt="Review-Bild"
                        className="max-w-xs rounded-lg border border-gray-200 cursor-pointer hover:opacity-80 transition-opacity"
                        onClick={() => {
                          setModalImage(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}${review.image_path}`);
                        }}
                      />
                      <p className="text-xs text-gray-500 mt-1">Klicken zum Vergrößern</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {totalPages > 1 && (
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={setCurrentPage}
        />
      )}
    </div>
  );

  const renderAdminTab = () => (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-medium mb-4">Neuen Admin-Benutzer erstellen</h3>

      <form onSubmit={handleAdminSubmit(handleCreateAdmin)} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Benutzername
          </label>
          <input
            {...registerAdmin('username', { required: 'Benutzername ist erforderlich' })}
            type="text"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {adminErrors.username && (
            <p className="mt-1 text-sm text-red-600">{adminErrors.username.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            E-Mail
          </label>
          <input
            {...registerAdmin('email', {
              required: 'E-Mail ist erforderlich',
              pattern: {
                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                message: 'Ungültige E-Mail-Adresse'
              }
            })}
            type="email"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {adminErrors.email && (
            <p className="mt-1 text-sm text-red-600">{adminErrors.email.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Passwort
          </label>
          <input
            {...registerAdmin('password', {
              required: 'Passwort ist erforderlich',
              minLength: {
                value: 6,
                message: 'Passwort muss mindestens 6 Zeichen lang sein'
              }
            })}
            type="password"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {adminErrors.password && (
            <p className="mt-1 text-sm text-red-600">{adminErrors.password.message}</p>
          )}
        </div>

        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Admin erstellen
        </button>
      </form>
    </div>
  );

  const renderExportTab = () => (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-medium mb-4">Vollständige Daten Sicherung & Wiederherstellung</h3>

      <div className="space-y-6">
        <div>
          <h4 className="font-medium text-gray-900 mb-2">📤 Vollständiger Export</h4>
          <p className="text-sm text-gray-600 mb-3">
            Exportiert alle Gästebucheinträge inklusive zugehöriger Kommentare als JSON-Datei.
            Diese Datei kann zur Datensicherung oder Wiederherstellung verwendet werden.
          </p>
          <div className="bg-blue-50 border border-blue-200 rounded-md p-3 mb-3">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-blue-800">Exportiert werden:</h3>
                <div className="mt-2 text-sm text-blue-700">
                  <ul className="list-disc list-inside space-y-1">
                    <li>Alle Gästebucheinträge (genehmigte und ausstehende)</li>
                    <li>Alle zugehörigen Kommentare</li>
                    <li>Bewertungen, Titel, Inhalte und Metadaten</li>
                    <li>Admin-Notizen und Moderations-Status</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          <button
            onClick={handleExportData}
            className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 flex items-center"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Vollständigen Export erstellen
          </button>
        </div>

        <hr className="my-6" />

        <div>
          <h4 className="font-medium text-gray-900 mb-2">📥 Daten Import & Wiederherstellung</h4>
          <p className="text-sm text-gray-600 mb-3">
            Importiert Gästebuchdaten aus einer JSON-Datei (erstellt durch den obigen Export).
            Sie können wählen, ob bestehende Daten ersetzt oder ergänzt werden sollen.
          </p>

          <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3 mb-3">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-yellow-800">⚠️ Wichtiger Hinweis</h3>
                <div className="mt-2 text-sm text-yellow-700">
                  <p>Beim Import werden Sie gefragt, ob bestehende Daten ersetzt werden sollen.
                  Die Ersetzung kann nicht rückgängig gemacht werden!</p>
                </div>
              </div>
            </div>
          </div>

          <input
            type="file"
            accept=".json"
            onChange={handleImportData}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 border border-gray-300 rounded-md"
          />
          <p className="mt-2 text-xs text-gray-500">
            Nur JSON-Dateien werden akzeptiert. Verwenden Sie Dateien, die durch den obigen Export erstellt wurden.
          </p>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <h1 className="text-2xl font-bold text-gray-900">
              Admin Dashboard
            </h1>

            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                Willkommen, {user?.username}
              </span>

              {/* Session Timer */}
              <SessionTimer className="hidden sm:flex" />

              {/* Session Extension Button - zeigt sich nur wenn Session bald abläuft */}
              <SessionExtensionButton className="hidden sm:flex" />

              <button
                onClick={() => navigate('/')}
                className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                ← Zurück zum Gästebuch
              </button>

              <button
                onClick={logout}
                className="bg-red-600 text-white px-4 py-2 rounded-md text-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                Abmelden
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Session Info */}
      <div className="sm:hidden bg-gray-50 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <SessionTimer showIcon={false} />
            <SessionExtensionButton />
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <nav className="flex space-x-8 mb-8">
          <button
            onClick={() => setActiveTab('moderation')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'moderation'
                ? 'border-orange-500 text-orange-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Moderation
          </button>

          <button
            onClick={() => setActiveTab('reviews')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'reviews'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Alle Bewertungen
          </button>

          <button
            onClick={() => setActiveTab('comments')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'comments'
                ? 'border-green-500 text-green-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Kommentare
          </button>

          <button
            onClick={() => setActiveTab('admin')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'admin'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Admin-Verwaltung
          </button>

          <button
            onClick={() => setActiveTab('export')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'export'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Import/Export
          </button>
        </nav>

        {/* Tab Content */}
        {activeTab === 'moderation' && <ModerationPanel />}
        {activeTab === 'reviews' && renderReviewsTab()}
        {activeTab === 'comments' && <AdminCommentsPanel />}
        {activeTab === 'admin' && renderAdminTab()}
        {activeTab === 'export' && renderExportTab()}
      </div>

      {/* Image Modal */}
      {modalImage && (
        <ImageModal
          imageSrc={modalImage}
          imageAlt="Review-Bild vergrößert"
          isOpen={!!modalImage}
          onClose={() => setModalImage(null)}
        />
      )}
    </div>
  );
};

export default AdminDashboard;
