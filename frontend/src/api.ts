import axios, { AxiosResponse } from 'axios';
import { 
  Review, 
  ReviewListResponse, 
  CreateReviewForm, 
  UpdateReviewForm,
  ReviewStats,
  Token,
  LoginForm,
  AdminReview,
  AdminUser
} from './types';

// Base API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

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
      
      // Prüfen ob wir uns im Admin-Bereich befinden
      if (window.location.pathname.startsWith('/admin') && window.location.pathname !== '/admin/login') {
        // Session-Ablauf-Nachricht in localStorage speichern
        localStorage.setItem('session_expired', 'true');
        window.location.href = '/admin/login';
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
    const response: AxiosResponse<Token> = await api.post('/api/admin/login', null, {
      params: credentials
    });
    return response.data;
  },

  // Admin User Management
  async createAdmin(data: { username: string; email: string; password: string }): Promise<AdminUser> {
    const response: AxiosResponse<AdminUser> = await api.post('/api/admin/users', data);
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

  // Import/Export
  async importData(importData: {
    reviews: Review[];
    exported_at: string;
  }): Promise<{ message: string; imported_count: number }> {
    const response = await api.post('/api/admin/import', importData);
    return response.data;
  },

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
