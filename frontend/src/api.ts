import axios, { AxiosResponse } from 'axios';
import {
    AdminReview,
    AdminUser,
    AdminUserListResponse,
    AdminUserUpdate,
    CreateReviewForm,
    FullExportData,
    FullImportData,
    ImportResult,
    LoginForm,
    RefreshToken,
    Review,
    ReviewListResponse,
    ReviewStats,
    Token,
    UpdateReviewForm
} from './types';

// Base API configuration - use relative URL when in combined container
const API_BASE_URL = process.env.REACT_APP_API_URL || (
  // Always use relative URLs when deployed (including localhost in combined container)
  ''
);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 || error.response?.status === 403) {
      // Session abgelaufen oder nicht authentifiziert
      localStorage.removeItem('admin_token');
      localStorage.removeItem('refresh_token');

      // Prüfen ob wir uns im Admin-Bereich befinden
      if (window.location.pathname.startsWith('/admin') && window.location.pathname !== '/admin/login') {
        // Session-Ablauf-Flag setzen für Session-Manager
        localStorage.setItem('session_expired', 'true');

        // Event auslösen für React-komponenten
        const sessionExpiredEvent = new CustomEvent('session-expired');
        window.dispatchEvent(sessionExpiredEvent);
      }
    }
    return Promise.reject(error);
  }
);

// Public API
export const publicApi = {
  // Reviews
  async getReviews(params: {
    page?: number;
    per_page?: number;
    rating?: number;
    search?: string;
    sort_by?: string;
    sort_order?: string;
  } = {}): Promise<ReviewListResponse> {
    const response: AxiosResponse<ReviewListResponse> = await api.get('/api/reviews', { params });
    return response.data;
  },

  async getReview(id: number): Promise<Review> {
    const response: AxiosResponse<Review> = await api.get(`/api/reviews/${id}`);
    return response.data;
  },

  async createReview(reviewData: CreateReviewForm): Promise<Review> {
    const response: AxiosResponse<Review> = await api.post('/api/reviews', reviewData);
    return response.data;
  },

  async uploadReviewImage(reviewId: number, file: File): Promise<{ image_path: string }> {
    const formData = new FormData();
    formData.append('file', file);

    const response: AxiosResponse<{ image_path: string }> = await api.post(
      `/api/reviews/${reviewId}/image`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },

  async getStats(): Promise<ReviewStats> {
    const response: AxiosResponse<ReviewStats> = await api.get('/api/stats');
    return response.data;
  },
};

// Admin API
export const adminApi = {
  // Auth
  async login(credentials: LoginForm): Promise<Token> {
    const response: AxiosResponse<Token> = await api.post('/api/admin/login', credentials);
    return response.data;
  },

  async refreshToken(refreshData: RefreshToken): Promise<Token> {
    const response: AxiosResponse<Token> = await api.post('/api/admin/refresh', refreshData);
    return response.data;
  },

  async getCurrentUser(): Promise<AdminUser> {
    const response: AxiosResponse<AdminUser> = await api.get('/api/admin/me');
    return response.data;
  },

  // Admin User Management
  async createAdmin(data: { username: string; email: string; password: string }): Promise<AdminUser> {
    const response: AxiosResponse<AdminUser> = await api.post('/api/admin/users', data);
    return response.data;
  },

  async getAdminUsers(params: {
    page?: number;
    per_page?: number;
  } = {}): Promise<AdminUserListResponse> {
    const response: AxiosResponse<AdminUserListResponse> = await api.get('/api/admin/users', { params });
    return response.data;
  },

  async getAdminUser(id: number): Promise<AdminUser> {
    const response: AxiosResponse<AdminUser> = await api.get(`/api/admin/users/${id}`);
    return response.data;
  },

  async updateAdminUser(id: number, data: AdminUserUpdate): Promise<AdminUser> {
    const response: AxiosResponse<AdminUser> = await api.put(`/api/admin/users/${id}`, data);
    return response.data;
  },

  async deleteAdminUser(id: number): Promise<{ message: string }> {
    const response: AxiosResponse<{ message: string }> = await api.delete(`/api/admin/users/${id}`);
    return response.data;
  },

  async deactivateAdminUser(id: number): Promise<AdminUser> {
    const response: AxiosResponse<AdminUser> = await api.post(`/api/admin/users/${id}/deactivate`);
    return response.data;
  },

  async activateAdminUser(id: number): Promise<AdminUser> {
    const response: AxiosResponse<AdminUser> = await api.post(`/api/admin/users/${id}/activate`);
    return response.data;
  },

  async changePassword(data: { old_password: string; new_password: string }): Promise<{ message: string }> {
    const response: AxiosResponse<{ message: string }> = await api.post('/api/admin/change-password', data);
    return response.data;
  },

  // Reviews Management
  async getReviews(params: {
    page?: number;
    per_page?: number;
    approved_only?: boolean;
  } = {}): Promise<ReviewListResponse> {
    const response: AxiosResponse<ReviewListResponse> = await api.get('/api/admin/reviews', { params });
    return response.data;
  },

  async updateReview(id: number, updateData: UpdateReviewForm): Promise<AdminReview> {
    const response: AxiosResponse<AdminReview> = await api.put(`/api/admin/reviews/${id}`, updateData);
    return response.data;
  },

  async deleteReview(id: number): Promise<{ message: string }> {
    const response: AxiosResponse<{ message: string }> = await api.delete(`/api/admin/reviews/${id}`);
    return response.data;
  },

  // Import/Export (Legacy functions - keeping exportData for backward compatibility)
  async exportData(): Promise<{
    reviews: Review[];
    stats: ReviewStats;
    exported_at: string;
  }> {
    const response = await api.get('/api/admin/export');
    return response.data;
  },

  async importReviews(importData: {
    reviews: Array<{
      name: string;
      rating: number;
      content: string;
      title?: string;
      email?: string;
      created_at?: string;
      import_source?: string;
      external_id?: string;
    }>;
    source: string;
  }): Promise<{ message: string; imported_count: number }> {
    const response = await api.post('/api/admin/reviews/import', importData);
    return response.data;
  },

  async getStats(): Promise<ReviewStats> {
    const response: AxiosResponse<ReviewStats> = await api.get('/api/admin/stats');
    return response.data;
  },

  async exportReviews(): Promise<Blob> {
    const response = await api.get('/api/admin/export', {
      responseType: 'blob',
    });
    return response.data;
  },

  // Vollständiger Export mit Kommentaren
  async exportFullData(): Promise<FullExportData> {
    const response: AxiosResponse<FullExportData> = await api.get('/api/admin/export/full');
    return response.data;
  },

  // Vollständiger Import mit Kommentaren
  async importFullData(importData: FullImportData, replaceExisting: boolean = false): Promise<ImportResult> {
    const response: AxiosResponse<ImportResult> = await api.post('/api/admin/import/full', importData, {
      params: { replace_existing: replaceExisting }
    });
    return response.data;
  },

  // Moderation
  async getPendingReviews(params: {
    page?: number;
    per_page?: number;
  } = {}): Promise<ReviewListResponse> {
    const response: AxiosResponse<ReviewListResponse> = await api.get('/api/admin/reviews/pending', { params });
    return response.data;
  },

  async approveReview(id: number): Promise<AdminReview> {
    const response: AxiosResponse<AdminReview> = await api.post(`/api/admin/reviews/${id}/approve`);
    return response.data;
  },

  async rejectReview(id: number): Promise<AdminReview> {
    const response: AxiosResponse<AdminReview> = await api.post(`/api/admin/reviews/${id}/reject`);
    return response.data;
  },
};

// Utility functions
export const apiUtils = {
  handleApiError(error: any): string {
    if (error.response?.data?.message) {
      return error.response.data.message;
    }
    if (error.message) {
      return error.message;
    }
    return 'Ein unbekannter Fehler ist aufgetreten';
  },

  downloadFile(blob: Blob, filename: string): void {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  },

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('de-DE', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  },

  formatRating(rating: number): string {
    return '★'.repeat(rating) + '☆'.repeat(5 - rating);
  },

  truncateText(text: string, maxLength: number = 200): string {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength).trim() + '...';
  },
};

export default api;
