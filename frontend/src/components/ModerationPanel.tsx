import React, { useState, useEffect, useCallback } from 'react';
import toast from 'react-hot-toast';
import { adminApi } from '../api';
import { Review } from '../types';
import RatingStars from './RatingStars';
import Pagination from './Pagination';

const ModerationPanel: React.FC = () => {
  const [pendingReviews, setPendingReviews] = useState<Review[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalReviews, setTotalReviews] = useState(0);

  const loadPendingReviews = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await adminApi.getPendingReviews({
        page: currentPage,
        per_page: 10
      });
      
      setPendingReviews(response.reviews);
      setTotalPages(Math.ceil(response.total / 10));
      setTotalReviews(response.total);
    } catch (error: any) {
      if (error.response?.status === 401 || error.response?.status === 403) {
        toast.error('Session abgelaufen. Sie werden zur Anmeldung weitergeleitet...');
      } else {
        toast.error('Fehler beim Laden der ausstehenden Bewertungen');
        console.error('Pending reviews fetch error:', error);
      }
    } finally {
      setIsLoading(false);
    }
  }, [currentPage]);

  useEffect(() => {
    loadPendingReviews();
  }, [loadPendingReviews]);

  const handleApproveReview = async (id: number) => {
    try {
      await adminApi.approveReview(id);
      toast.success('Bewertung genehmigt');
      loadPendingReviews();
    } catch (error) {
      toast.error('Fehler beim Genehmigen der Bewertung');
    }
  };

  const handleRejectReview = async (id: number) => {
    if (!window.confirm('Sind Sie sicher, dass Sie diese Bewertung ablehnen möchten?')) {
      return;
    }
    
    try {
      await adminApi.rejectReview(id);
      toast.success('Bewertung abgelehnt');
      loadPendingReviews();
    } catch (error) {
      toast.error('Fehler beim Ablehnen der Bewertung');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-lg font-medium">Moderationsbereich</h3>
            <p className="text-sm text-gray-600 mt-1">
              {totalReviews === 0 
                ? 'Keine ausstehenden Bewertungen' 
                : `${totalReviews} Bewertung${totalReviews !== 1 ? 'en' : ''} warten auf Freischaltung`
              }
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={loadPendingReviews}
              disabled={isLoading}
              className="px-4 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {isLoading ? 'Lädt...' : 'Aktualisieren'}
            </button>
          </div>
        </div>
      </div>

      {/* Pending Reviews List */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-4 py-5 sm:p-6">
          {isLoading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-2 text-gray-600">Lade ausstehende Bewertungen...</p>
            </div>
          ) : pendingReviews.length === 0 ? (
            <div className="text-center py-8">
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
                <svg
                  className="h-6 w-6 text-green-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </div>
              <h3 className="mt-2 text-sm font-medium text-gray-900">
                Alle Bewertungen bearbeitet
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                Momentan gibt es keine ausstehenden Bewertungen zur Moderation.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {pendingReviews.map((review) => (
                <div key={review.id} className="border border-orange-200 rounded-lg p-4 bg-orange-50">
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h4 className="font-semibold text-gray-900">{review.name}</h4>
                        <RatingStars rating={review.rating} readonly />
                        <span className="px-2 py-1 bg-orange-100 text-orange-800 text-xs rounded-full">
                          Ausstehend
                        </span>
                      </div>
                      
                      {review.title && (
                        <h5 className="text-sm font-medium text-gray-700 mb-1">
                          {review.title}
                        </h5>
                      )}
                      
                      <p className="text-gray-700 mb-2">{review.content}</p>
                      
                      <div className="text-xs text-gray-500">
                        Eingereicht am: {new Date(review.created_at).toLocaleDateString('de-DE', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </div>
                      
                      {review.email && (
                        <div className="text-xs text-gray-500 mt-1">
                          E-Mail: {review.email}
                        </div>
                      )}
                    </div>
                    
                    <div className="flex flex-col space-y-2 ml-4">
                      <button
                        onClick={() => handleApproveReview(review.id)}
                        className="px-4 py-2 text-sm bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
                      >
                        ✓ Genehmigen
                      </button>
                      
                      <button
                        onClick={() => handleRejectReview(review.id)}
                        className="px-4 py-2 text-sm bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
                      >
                        ✗ Ablehnen
                      </button>
                    </div>
                  </div>
                  
                  {review.image_path && (
                    <div className="mt-3">
                      <img
                        src={`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}${review.image_path}`}
                        alt="Review-Bild"
                        className="max-w-xs rounded-lg border border-gray-200"
                      />
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
};

export default ModerationPanel;
