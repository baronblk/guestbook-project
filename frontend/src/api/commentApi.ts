import { CommentAdminListResponse, CommentCreate, CommentListResponse, CommentResponse } from '../types/comments';

const API_BASE_URL = process.env.REACT_APP_API_URL || '';

export const commentApi = {
  // Kommentar erstellen
  async createComment(comment: CommentCreate): Promise<CommentResponse> {
    const response = await fetch(`${API_BASE_URL}/api/reviews/${comment.review_id}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(comment),
    });

    if (!response.ok) {
      const error = await response.json();
      throw { response: { data: error } };
    }

    return response.json();
  },

  // Kommentare für eine Bewertung abrufen
  async getCommentsByReview(
    reviewId: number,
    page: number = 1,
    perPage: number = 10
  ): Promise<CommentListResponse> {
    const response = await fetch(
      `${API_BASE_URL}/api/reviews/${reviewId}/comments?page=${page}&per_page=${perPage}`
    );

    if (!response.ok) {
      throw new Error('Fehler beim Laden der Kommentare');
    }

    return response.json();
  },

  // Admin: Alle Kommentare mit Review-Informationen abrufen
  async getComments(
    page: number = 1,
    perPage: number = 10,
    token: string
  ): Promise<CommentAdminListResponse> {
    const response = await fetch(
      `${API_BASE_URL}/api/admin/comments?page=${page}&per_page=${perPage}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error('Fehler beim Laden der Kommentare');
    }

    return response.json();
  },

  // Admin: Pending Kommentare mit Review-Informationen abrufen
  async getPendingComments(
    page: number = 1,
    perPage: number = 10,
    token: string
  ): Promise<CommentAdminListResponse> {
    const response = await fetch(
      `${API_BASE_URL}/api/admin/comments/pending?page=${page}&per_page=${perPage}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error('Fehler beim Laden der pending Kommentare');
    }

    return response.json();
  },

  // Admin: Kommentar genehmigen
  async approveComment(commentId: number, token: string): Promise<CommentResponse> {
    const response = await fetch(`${API_BASE_URL}/api/admin/comments/${commentId}/approve`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Fehler beim Genehmigen des Kommentars');
    }

    return response.json();
  },

  // Admin: Kommentar löschen
  async deleteComment(commentId: number, token: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/admin/comments/${commentId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Fehler beim Löschen des Kommentars');
    }
  },
};
