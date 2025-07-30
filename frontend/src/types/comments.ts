export interface CommentBase {
  name: string;
  email?: string;
  content: string;
}

export interface CommentCreate extends CommentBase {
  review_id: number;
}

export interface CommentResponse extends CommentBase {
  id: number;
  review_id: number;
  created_at: string;
  updated_at?: string;
  is_approved: boolean;
}

export interface CommentAdminResponse extends CommentResponse {
  admin_notes?: string;
  ip_address?: string;
}

export interface CommentWithReviewInfo extends CommentAdminResponse {
  review_author: string;
  review_title?: string;
  review_rating: number;
}

export interface CommentUpdate {
  name?: string;
  email?: string;
  content?: string;
  is_approved?: boolean;
  admin_notes?: string;
}

export interface CommentListResponse {
  comments: CommentResponse[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface CommentAdminListResponse {
  comments: CommentWithReviewInfo[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}
