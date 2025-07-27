import React, { useEffect, useState } from 'react';
import { useReviewStore } from '../store/reviewStore';
import RatingStars from './RatingStars';
import Pagination from './Pagination';
import ImageModal from './ImageModal';
import { apiUtils } from '../api';

interface ReviewListProps {
  embedded?: boolean;
}

const ReviewList: React.FC<ReviewListProps> = ({ embedded = false }) => {
  const {
    reviews,
    loading,
    error,
    pagination,
    filters,
    fetchReviews,
    setPage,
    clearError,
    updateFilters,
  } = useReviewStore();

  // Local state for filter controls - Simplified
  const [selectedRating, setSelectedRating] = useState<number | undefined>(filters.rating);
  
  // Modal state for image viewing
  const [modalImage, setModalImage] = useState<{ src: string; alt: string } | null>(null);

  useEffect(() => {
    fetchReviews();
  }, [fetchReviews]);

  // Handler für Filter-Updates - Simplified
  const handleFilterUpdate = () => {
    const newFilters = {
      rating: selectedRating || undefined,
      sort_by: 'created_at' as const,
      sort_order: 'desc' as const,
    };
    updateFilters(newFilters);
  };

  // Filter zurücksetzen - Simplified
  const resetFilters = () => {
    setSelectedRating(undefined);
    updateFilters({
      rating: undefined,
      sort_by: 'created_at' as const,
      sort_order: 'desc' as const,
    });
  };

  if (loading && reviews.length === 0) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="spinner" />
        <span className="ml-2 text-gray-600">Bewertungen werden geladen...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">
              Fehler beim Laden der Bewertungen
            </h3>
            <div className="mt-2 text-sm text-red-700">
              <p>{error}</p>
            </div>
            <div className="mt-4">
              <button
                type="button"
                className="bg-red-100 px-2 py-1 text-sm text-red-800 rounded hover:bg-red-200"
                onClick={() => {
                  clearError();
                  fetchReviews();
                }}
              >
                Erneut versuchen
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (reviews.length === 0) {
    return (
      <div className="text-center py-12">
        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-1l-4 4z"
          />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-gray-900">
          Keine Bewertungen vorhanden
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          Seien Sie der erste, der eine Bewertung abgibt!
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Ultra-Minimal Filter Controls */}
      {!embedded && (
        <div className="flex flex-wrap items-center gap-6 py-4 border-b border-gray-200 mb-6">
          
          {/* Star Rating Filter - Clickable Stars */}
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-600">Filter ab:</span>
            <div className="flex items-center gap-1">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  onClick={() => {
                    const newRating = selectedRating === star ? undefined : star;
                    setSelectedRating(newRating);
                    const newFilters = {
                      rating: newRating || undefined,
                      sort_by: 'created_at' as const,
                      sort_order: 'desc' as const,
                    };
                    updateFilters(newFilters);
                  }}
                  className={`text-xl transition-all duration-150 hover:scale-110 ${
                    selectedRating && star <= selectedRating
                      ? 'text-yellow-500'
                      : 'text-gray-300 hover:text-yellow-400'
                  }`}
                  title={`${selectedRating === star ? 'Filter entfernen' : `Ab ${star} ${star === 1 ? 'Stern' : 'Sterne'} filtern`}`}
                >
                  ⭐
                </button>
              ))}
              {selectedRating && (
                <button
                  onClick={() => {
                    setSelectedRating(undefined);
                    const newFilters = {
                      rating: undefined,
                      sort_by: 'created_at' as const,
                      sort_order: 'desc' as const,
                    };
                    updateFilters(newFilters);
                  }}
                  className="ml-2 text-xs text-gray-500 hover:text-gray-700 underline"
                >
                  alle
                </button>
              )}
            </div>
          </div>

          {/* Results Counter */}
          <div className="ml-auto text-sm text-gray-500">
            <span className="font-medium text-gray-900">{reviews.length}</span> von <span className="font-medium">{pagination.total}</span> Bewertungen
          </div>
        </div>
      )}

      {/* Reviews */}
      <div className="space-y-6">
        {reviews.map((review, index) => (
          <div
            key={review.id}
            className="group relative bg-white rounded-2xl border transition-all duration-300 hover:shadow-xl hover:-translate-y-1 border-gray-200 shadow-md hover:border-gray-300"
          >
            <div className="p-6">
              {/* Header mit Avatar */}
              <div className="flex items-start space-x-4 mb-4">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg bg-gradient-to-br from-blue-500 to-purple-600">
                    {review.name.charAt(0).toUpperCase()}
                  </div>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 truncate">
                        {review.name}
                      </h3>
                      {review.title && (
                        <h4 className="text-sm text-gray-600 mt-0.5 font-medium">
                          {review.title}
                        </h4>
                      )}
                    </div>
                    <div className="flex-shrink-0 ml-4">
                      <RatingStars rating={review.rating} size="sm" />
                    </div>
                  </div>
                </div>
              </div>

              {/* Content */}
              <div className="mb-4">
                <div className="text-gray-700 leading-relaxed">
                  <p className="whitespace-pre-wrap">
                    {embedded 
                      ? apiUtils.truncateText(review.content, 150)
                      : review.content
                    }
                  </p>
                </div>
              </div>

              {/* Image */}
              {review.image_path && (
                <div className="mb-4">
                  <div 
                    className="relative overflow-hidden rounded-xl group cursor-pointer"
                    onClick={() => {
                      console.log('Image clicked, opening modal for:', review.image_path);
                      setModalImage({
                        src: `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}${review.image_path}`,
                        alt: `Bewertungsbild von ${review.name}`
                      });
                    }}
                  >
                    <img
                      src={`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}${review.image_path}`}
                      alt="Bewertungsbild"
                      className="w-full h-48 object-cover transition-all duration-300 group-hover:scale-105"
                    />
                    {/* Hover Overlay */}
                    <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300 flex items-center justify-center pointer-events-none">
                      <div className="transform scale-0 group-hover:scale-100 transition-transform duration-300 bg-white bg-opacity-90 rounded-full p-3">
                        <svg className="w-6 h-6 text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
                        </svg>
                      </div>
                    </div>
                    {/* Image Info Badge */}
                    <div className="absolute bottom-2 left-2 bg-black bg-opacity-50 text-white text-xs px-2 py-1 rounded pointer-events-none">
                      📷 Klicken zum Vergrößern
                    </div>
                  </div>
                </div>
              )}

              {/* Footer */}
              <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                <div className="flex items-center space-x-2 text-sm text-gray-500">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <time dateTime={review.created_at}>
                    {apiUtils.formatDate(review.created_at)}
                  </time>
                </div>
                
                {/* Review-Nummer für bessere Übersicht */}
                <div className="flex items-center space-x-2">
                  <span className="text-xs text-gray-400 font-medium">
                    #{String(index + 1).padStart(2, '0')}
                  </span>
                  <div className="w-2 h-2 rounded-full bg-gray-300"></div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Pagination (nur wenn nicht embedded) */}
      {!embedded && pagination.total_pages > 1 && (
        <Pagination
          currentPage={pagination.page}
          totalPages={pagination.total_pages}
          onPageChange={setPage}
        />
      )}

      {/* Loading overlay für zusätzliche Seiten */}
      {loading && reviews.length > 0 && (
        <div className="flex justify-center py-4">
          <div className="spinner" />
          <span className="ml-2 text-gray-600">Lädt...</span>
        </div>
      )}

      {/* Image Modal */}
      {modalImage && (
        <>
          {console.log('Rendering ImageModal with:', modalImage)}
          <ImageModal
            isOpen={!!modalImage}
            imageSrc={modalImage.src}
            imageAlt={modalImage.alt}
            onClose={() => {
              console.log('Closing modal');
              setModalImage(null);
            }}
          />
        </>
      )}
    </div>
  );
};

export default ReviewList;
