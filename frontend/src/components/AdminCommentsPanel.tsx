import React, { useState, useEffect } from 'react';
import { commentApi } from '../api/commentApi';
import { useAuthStore } from '../store/authStore';
import { CommentResponse, CommentAdminResponse } from '../types/comments';
import { apiUtils } from '../api';

const AdminCommentsPanel: React.FC = () => {
  const { token } = useAuthStore();
  const [comments, setComments] = useState<CommentResponse[]>([]);
  const [pendingComments, setPendingComments] = useState<CommentResponse[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  // Tab-Auswahl persistent speichern
  const getInitialTab = () => {
    const saved = localStorage.getItem('adminCommentsTab');
    return saved === 'all' ? 'all' : 'pending';
  };
  const [activeTab, setActiveTab] = useState<'pending' | 'all'>(getInitialTab());
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 10,
    total: 0,
    total_pages: 0
  });
  const [allCount, setAllCount] = useState<number>(0);
  const [pendingCount, setPendingCount] = useState<number>(0);

  const fetchComments = async (tab: 'pending' | 'all' = activeTab, page = 1) => {
    if (!token) return;
    
    setLoading(true);
    setError(null);

    try {
      let response;
      if (tab === 'pending') {
        response = await commentApi.getPendingComments(page, pagination.per_page, token);
        setPendingComments(response.comments);
      } else {
        response = await commentApi.getComments(page, pagination.per_page, token);
        setComments(response.comments);
      }

      setPagination({
        page: response.page,
        per_page: response.per_page,
        total: response.total,
        total_pages: response.total_pages
      });
      // Tab-Counts synchron aktualisieren
      await fetchTabCounts();
    } catch (err: any) {
      setError(err.message || 'Fehler beim Laden der Kommentare');
    } finally {
      setLoading(false);
    }
  };

  // Neue Funktion: Tab-Counts aus Endpunkten holen
  const fetchTabCounts = async () => {
    if (!token) return;
    try {
      const [allRes, pendingRes] = await Promise.all([
        fetch('/api/admin/comments/count/all', {
          headers: { Authorization: `Bearer ${token}` }
        }).then(r => r.json()),
        fetch('/api/admin/comments/count/pending', {
          headers: { Authorization: `Bearer ${token}` }
        }).then(r => r.json())
      ]);
      setAllCount(allRes.count ?? 0);
      setPendingCount(pendingRes.count ?? 0);
    } catch (err) {
      // Fehler ignorieren, falls Backend nicht erreichbar
    }
  };

  const handleApprove = async (commentId: number) => {
    if (!token) return;

    try {
      await commentApi.approveComment(commentId, token);
      
      // Aktualisiere Listen
      if (activeTab === 'pending') {
        setPendingComments(prev => prev.filter(c => c.id !== commentId));
      }
      await fetchComments('all', 1); // Refresh all comments
      await fetchTabCounts();
    } catch (err: any) {
      setError(err.message || 'Fehler beim Genehmigen des Kommentars');
    }
  };

  const handleDelete = async (commentId: number) => {
    if (!token) return;
    
    if (!window.confirm('Möchten Sie diesen Kommentar wirklich löschen?')) {
      return;
    }

    try {
      await commentApi.deleteComment(commentId, token);
      
      // Aktualisiere Listen
      if (activeTab === 'pending') {
        setPendingComments(prev => prev.filter(c => c.id !== commentId));
      } else {
        setComments(prev => prev.filter(c => c.id !== commentId));
      }
      await fetchTabCounts();
    } catch (err: any) {
      setError(err.message || 'Fehler beim Löschen des Kommentars');
    }
  };

  const handleTabChange = (tab: 'pending' | 'all') => {
    setActiveTab(tab);
    localStorage.setItem('adminCommentsTab', tab);
    setPagination(prev => ({ ...prev, page: 1 }));
    // Tab-Counts und Kommentare synchron laden
    fetchComments(tab, 1);
  };

  useEffect(() => {
    // Nur laden, wenn Tab sich ändert (Tab-Wechsel oder Token-Wechsel)
    fetchComments(activeTab, 1);
  }, [activeTab, token]);

  // Tab-Counts direkt beim ersten Rendern laden
  useEffect(() => {
    // Tab-Counts und Kommentare initial laden
    fetchComments(activeTab, 1);
  }, [token]);

  const currentComments = activeTab === 'pending' ? pendingComments : comments;

  return (
    <div className="bg-white rounded-lg shadow">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Kommentar-Verwaltung</h2>
        <p className="text-sm text-gray-600 mt-1">
          Verwalten Sie Kommentare zu Bewertungen
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-8 px-6" aria-label="Tabs">
          <button
            onClick={() => handleTabChange('pending')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'pending'
                ? 'border-indigo-500 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Ausstehend ({pendingCount})
          </button>
          <button
            onClick={() => handleTabChange('all')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'all'
                ? 'border-indigo-500 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Alle Kommentare ({allCount})
          </button>
        </nav>
      </div>

      {/* Content */}
      <div className="p-6">
        {error && (
          <div className="mb-4 bg-red-50 border border-red-200 rounded-md p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Fehler</h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>{error}</p>
                </div>
                <div className="mt-4">
                  <button
                    type="button"
                    onClick={() => setError(null)}
                    className="bg-red-50 text-red-800 rounded-md p-2 inline-flex items-center text-sm font-medium hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  >
                    Schließen
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
            <span className="ml-2 text-gray-600">Kommentare werden geladen...</span>
          </div>
        ) : currentComments.length === 0 ? (
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">
              {activeTab === 'pending' ? 'Keine ausstehenden Kommentare' : 'Keine Kommentare vorhanden'}
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              {activeTab === 'pending' 
                ? 'Alle Kommentare wurden bereits moderiert.' 
                : 'Es wurden noch keine Kommentare erstellt.'
              }
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {currentComments.map((comment) => (
              <div
                key={comment.id}
                className={`border rounded-lg p-4 ${
                  !comment.is_approved ? 'border-yellow-200 bg-yellow-50' : 'border-gray-200'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    {/* Comment Header */}
                    <div className="flex items-center space-x-2 mb-2">
                      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center text-white text-sm font-semibold">
                        {comment.name.charAt(0).toUpperCase()}
                      </div>
                      <div>
                        <h4 className="text-sm font-semibold text-gray-900">
                          {comment.name}
                        </h4>
                        <p className="text-xs text-gray-500">
                          Review ID: {comment.review_id} • {apiUtils.formatDate(comment.created_at)}
                        </p>
                      </div>
                      {!comment.is_approved && (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                          Ausstehend
                        </span>
                      )}
                    </div>

                    {/* Comment Content */}
                    <div className="mb-3">
                      <p className="text-sm text-gray-700 whitespace-pre-wrap">
                        {comment.content}
                      </p>
                    </div>

                    {/* Comment Email */}
                    {comment.email && (
                      <div className="text-xs text-gray-500 mb-2">
                        E-Mail: {comment.email}
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex-shrink-0 ml-4">
                    <div className="flex space-x-2">
                      {!comment.is_approved && (
                        <button
                          onClick={() => handleApprove(comment.id)}
                          className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                        >
                          Genehmigen
                        </button>
                      )}
                      <button
                        onClick={() => handleDelete(comment.id)}
                        className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                      >
                        Löschen
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Pagination */}
        {pagination.total_pages > 1 && (
          <div className="flex items-center justify-between pt-6">
            <div className="flex-1 flex justify-between sm:hidden">
              <button
                onClick={() => fetchComments(activeTab, pagination.page - 1)}
                disabled={pagination.page === 1}
                className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Vorherige
              </button>
              <button
                onClick={() => fetchComments(activeTab, pagination.page + 1)}
                disabled={pagination.page === pagination.total_pages}
                className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Nächste
              </button>
            </div>
            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-gray-700">
                  Zeige <span className="font-medium">{(pagination.page - 1) * pagination.per_page + 1}</span> bis{' '}
                  <span className="font-medium">
                    {Math.min(pagination.page * pagination.per_page, pagination.total)}
                  </span>{' '}
                  von <span className="font-medium">{pagination.total}</span> Kommentaren
                </p>
              </div>
              <div>
                <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                  <button
                    onClick={() => fetchComments(activeTab, pagination.page - 1)}
                    disabled={pagination.page === 1}
                    className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <span className="sr-only">Vorherige</span>
                    <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </button>
                  <span className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
                    Seite {pagination.page} von {pagination.total_pages}
                  </span>
                  <button
                    onClick={() => fetchComments(activeTab, pagination.page + 1)}
                    disabled={pagination.page === pagination.total_pages}
                    className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <span className="sr-only">Nächste</span>
                    <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                    </svg>
                  </button>
                </nav>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminCommentsPanel;
