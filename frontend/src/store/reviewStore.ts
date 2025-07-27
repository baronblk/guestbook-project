import { create } from 'zustand';
import { ReviewStore, ReviewFilters, ReviewFilter, CreateReviewForm } from '../types';
import { publicApi, adminApi, apiUtils } from '../api';

export const useReviewStore = create<ReviewStore>((set, get) => ({
  reviews: [],
  loading: false,
  error: null,
  filter: {
    sort_by: 'created_at',
    sort_order: 'desc',
  },
  filters: {
    sort_by: 'created_at',
    sort_order: 'desc',
  },
  pagination: {
    page: 1,
    per_page: 10,
    total: 0,
    total_pages: 0,
  },

  fetchReviews: async (filter?: ReviewFilter) => {
    set({ loading: true, error: null });
    try {
      const { filters, pagination } = get();
      const params = {
        page: pagination.page,
        per_page: pagination.per_page,
        ...filters,
        ...filter,
      };

      const response = await publicApi.getReviews(params);
      
      set({
        reviews: response.reviews,
        pagination: {
          page: response.page,
          per_page: response.per_page,
          total: response.total,
          total_pages: response.total_pages,
        },
        loading: false,
      });

      return { total: response.total, reviews: response.reviews };
    } catch (error) {
      set({
        error: apiUtils.handleApiError(error),
        loading: false,
      });
      throw error;
    }
  },

  createReview: async (reviewData: CreateReviewForm) => {
    try {
      const review = await publicApi.createReview(reviewData);
      
      // Upload image if provided
      if (reviewData.image) {
        await publicApi.uploadReviewImage(review.id, reviewData.image);
      }

      // Refresh reviews
      await get().fetchReviews();
      return true;
    } catch (error) {
      set({ error: apiUtils.handleApiError(error) });
      return false;
    }
  },

  deleteReview: async (id: number) => {
    try {
      await adminApi.deleteReview(id);
      // Remove from local state
      set(state => ({
        reviews: state.reviews.filter(review => review.id !== id)
      }));
    } catch (error) {
      set({ error: apiUtils.handleApiError(error) });
      throw error;
    }
  },

  toggleReviewVisibility: async (id: number) => {
    try {
      const review = get().reviews.find(r => r.id === id);
      if (!review) return;

      await adminApi.updateReview(id, { is_approved: !review.is_approved });
      
      // Update local state
      set(state => ({
        reviews: state.reviews.map(r => 
          r.id === id 
            ? { ...r, is_approved: !r.is_approved, is_visible: !r.is_approved }
            : r
        )
      }));
    } catch (error) {
      set({ error: apiUtils.handleApiError(error) });
      throw error;
    }
  },

  updateFilters: (newFilters: Partial<ReviewFilters>) => {
    set(state => ({
      filters: { ...state.filters, ...newFilters },
      filter: { ...state.filter, ...newFilters },
      pagination: { ...state.pagination, page: 1 }, // Reset to first page
    }));
    // Auto-fetch with new filters
    setTimeout(() => get().fetchReviews(), 100);
  },

  setFilter: (newFilter: ReviewFilters) => {
    set(state => ({
      filter: newFilter,
      filters: newFilter,
      pagination: { ...state.pagination, page: 1 },
    }));
  },

  setPage: (page: number) => {
    set(state => ({
      pagination: { ...state.pagination, page },
    }));
    get().fetchReviews();
  },

  clearError: () => set({ error: null }),
}));
