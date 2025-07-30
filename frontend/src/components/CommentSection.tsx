import React, { useState, useEffect } from 'react';
import { commentApi } from '../api/commentApi';
import { CommentResponse, CommentCreate } from '../types/comments';
import { apiUtils } from '../api';

interface CommentSectionProps {
  reviewId: number;
  reviewAuthor: string;
}

const CommentSection: React.FC<CommentSectionProps> = ({ reviewId, reviewAuthor }) => {
  const [comments, setComments] = useState<CommentResponse[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    content: ''
  });
  const [submitting, setSubmitting] = useState(false);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(false);

  const fetchComments = async (pageNumber = 1) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await commentApi.getCommentsByReview(reviewId, pageNumber, 10);
      
      if (pageNumber === 1) {
        setComments(response.comments);
      } else {
        setComments(prev => [...prev, ...response.comments]);
      }
      
      setTotal(response.total);
      setHasMore(response.page < response.total_pages);
      setPage(pageNumber);
    } catch (err) {
      setError('Fehler beim Laden der Kommentare');
      console.error('Error fetching comments:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name.trim() || !formData.content.trim()) {
      setError('Name und Kommentar sind erforderlich');
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      const commentData: CommentCreate = {
        review_id: reviewId,
        name: formData.name.trim(),
        email: formData.email.trim() || undefined,
        content: formData.content.trim()
      };

      await commentApi.createComment(commentData);
      
      // Reset form
      setFormData({ name: '', email: '', content: '' });
      setShowForm(false);
      
      // Refresh comments
      await fetchComments(1);
      
      // Show success message
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Fehler beim Erstellen des Kommentars');
    } finally {
      setSubmitting(false);
    }
  };

  const loadMoreComments = () => {
    if (!loading && hasMore) {
      fetchComments(page + 1);
    }
  };

  useEffect(() => {
    fetchComments(1);
  }, [reviewId]);

  return (
    <div className="mt-6 pt-6 border-t border-gray-200">
      {/* Comment Header */}
      <div className="flex items-center justify-between mb-4">
        <h4 className="text-lg font-semibold text-gray-900">
          Kommentare {total > 0 && `(${total})`}
        </h4>
        <button
          onClick={() => setShowForm(!showForm)}
          className="text-sm bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors duration-200"
        >
          {showForm ? 'Abbrechen' : 'Kommentieren'}
        </button>
      </div>

      {/* Comment Form */}
      {showForm && (
        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="comment-name" className="block text-sm font-medium text-gray-700 mb-1">
                  Name *
                </label>
                <input
                  id="comment-name"
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Ihr Name"
                  maxLength={100}
                  required
                />
              </div>
              <div>
                <label htmlFor="comment-email" className="block text-sm font-medium text-gray-700 mb-1">
                  E-Mail (optional)
                </label>
                <input
                  id="comment-email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="ihre@email.de"
                />
              </div>
            </div>
            <div>
              <label htmlFor="comment-content" className="block text-sm font-medium text-gray-700 mb-1">
                Kommentar *
              </label>
              <textarea
                id="comment-content"
                value={formData.content}
                onChange={(e) => setFormData(prev => ({ ...prev, content: e.target.value }))}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                placeholder={`Antworten Sie auf ${reviewAuthor}s Bewertung...`}
                maxLength={2000}
                required
              />
              <div className="text-right text-xs text-gray-500 mt-1">
                {formData.content.length}/2000 Zeichen
              </div>
            </div>
            
            {error && (
              <div className="text-red-600 text-sm bg-red-50 p-2 rounded">
                {error}
              </div>
            )}
            
            <div className="flex justify-end space-x-2">
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="px-4 py-2 text-gray-600 bg-gray-200 hover:bg-gray-300 rounded-md transition-colors duration-200"
              >
                Abbrechen
              </button>
              <button
                type="submit"
                disabled={submitting}
                className="px-4 py-2 bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white rounded-md transition-colors duration-200 flex items-center"
              >
                {submitting ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Wird gesendet...
                  </>
                ) : (
                  'Kommentar senden'
                )}
              </button>
            </div>
          </form>
          
          <div className="mt-2 text-xs text-gray-500">
            * Ihr Kommentar wird nach Prüfung freigeschaltet
          </div>
        </div>
      )}

      {/* Comments List */}
      {loading && comments.length === 0 ? (
        <div className="flex justify-center py-4">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
          <span className="ml-2 text-gray-600">Kommentare werden geladen...</span>
        </div>
      ) : comments.length > 0 ? (
        <div className="space-y-4">
          {comments.map((comment, index) => (
            <div key={comment.id} className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center text-white text-sm font-semibold">
                    {comment.name.charAt(0).toUpperCase()}
                  </div>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-2 mb-1">
                    <h5 className="text-sm font-semibold text-gray-900">
                      {comment.name}
                    </h5>
                    <span className="text-xs text-gray-500">
                      {apiUtils.formatDate(comment.created_at)}
                    </span>
                  </div>
                  <p className="text-sm text-gray-700 whitespace-pre-wrap">
                    {comment.content}
                  </p>
                </div>
              </div>
            </div>
          ))}
          
          {/* Load More Button */}
          {hasMore && (
            <div className="flex justify-center mt-4">
              <button
                onClick={loadMoreComments}
                disabled={loading}
                className="px-4 py-2 text-sm bg-gray-200 hover:bg-gray-300 disabled:bg-gray-100 text-gray-700 rounded-md transition-colors duration-200"
              >
                {loading ? 'Lädt...' : 'Weitere Kommentare laden'}
              </button>
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-6 text-gray-500">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <p className="mt-2">Noch keine Kommentare vorhanden.</p>
          <p className="text-sm">Seien Sie der Erste, der kommentiert!</p>
        </div>
      )}
    </div>
  );
};

export default CommentSection;
