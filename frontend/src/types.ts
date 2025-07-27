// API Response Types
export interface Review {
  id: number;
  name: string;
  email?: string;
  rating: number;
  title?: string;
  content: string;
  comment?: string;  // Alternative to content
  image_path?: string;
  image?: string;  // Full URL for display
  created_at: string;
  updated_at?: string;
  is_approved: boolean;
  is_visible?: boolean;  // Alternative to is_approved
}

export interface AdminReview extends Review {
  admin_notes?: string;
  import_source?: string;
  external_id?: string;
  ip_address?: string;
}

export interface ReviewListResponse {
  reviews: Review[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface ReviewStats {
  total_reviews: number;
  approved_reviews?: number;
  pending_reviews?: number;
  average_rating: number;
  rating_distribution: Record<string, number>;
}

// Form Types
export interface CreateReviewForm {
  name: string;
  email?: string;
  rating: number;
  title?: string;
  content: string;
  image?: File;
}

export interface UpdateReviewForm {
  name?: string;
  email?: string;
  rating?: number;
  title?: string;
  content?: string;
  is_approved?: boolean;
  admin_notes?: string;
}

// Auth Types
export interface AdminUser {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  last_login?: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface LoginForm {
  username: string;
  password: string;
}

// Filter Types
export interface ReviewFilters {
  rating?: number;
  min_rating?: number;
  is_visible?: boolean;
  search?: string;
  sort_by?: 'created_at' | 'rating' | 'name';
  sort_order?: 'asc' | 'desc';
}

export interface ReviewFilter extends ReviewFilters {
  page?: number;
  limit?: number;
}

// Import/Export Types
export interface ImportExportData {
  reviews: Review[];
  stats?: ReviewStats;
  exported_at: string;
}

// Component Props Types
export interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export interface RatingStarsProps {
  rating: number;
  maxRating?: number;
  size?: 'sm' | 'md' | 'lg';
  interactive?: boolean;
  readonly?: boolean;
  onChange?: (rating: number) => void;
}

export interface ReviewCardProps {
  review: Review;
  showAdminControls?: boolean;
  onEdit?: (review: Review) => void;
  onDelete?: (reviewId: number) => void;
  onToggleApproval?: (reviewId: number) => void;
  onToggleFeatured?: (reviewId: number) => void;
}

// Store Types
export interface ReviewStore {
  reviews: Review[];
  loading: boolean;
  error: string | null;
  filter: ReviewFilters;
  filters: ReviewFilters;
  pagination: {
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
  };
  
  // Actions
  fetchReviews: (filter?: ReviewFilter) => Promise<{ total: number; reviews: Review[] }>;
  createReview: (review: CreateReviewForm) => Promise<boolean>;
  deleteReview: (id: number) => Promise<void>;
  toggleReviewVisibility: (id: number) => Promise<void>;
  updateFilters: (filters: Partial<ReviewFilters>) => void;
  setFilter: (filter: ReviewFilters) => void;
  setPage: (page: number) => void;
  clearError: () => void;
}

export interface AuthStore {
  user: AdminUser | null;
  token: string | null;
  loading: boolean;
  error: string | null;
  
  // Actions
  login: (credentials: LoginForm) => Promise<boolean>;
  logout: () => void;
  checkAuth: () => Promise<void>;
  validateSession: () => Promise<boolean>;
  clearError: () => void;
}

// Utility Types
export type SortDirection = 'asc' | 'desc';
export type RatingValue = 1 | 2 | 3 | 4 | 5;

// API Error Type
export interface ApiError {
  message: string;
  status_code: number;
}
