import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { AuthStore, LoginForm, AdminUser } from '../types';
import { adminApi, apiUtils } from '../api';

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      loading: false,
      error: null,

      login: async (credentials: LoginForm) => {
        set({ loading: true, error: null });
        try {
          const tokenResponse = await adminApi.login(credentials);
          
          // Store token
          localStorage.setItem('admin_token', tokenResponse.access_token);
          
          set({
            token: tokenResponse.access_token,
            user: { 
              username: credentials.username,
              // Mock user data - in real app, fetch user details
              id: 1,
              email: '',
              is_active: true,
              is_superuser: true,
              created_at: new Date().toISOString()
            } as AdminUser,
            loading: false,
          });

          return true;
        } catch (error) {
          set({
            error: apiUtils.handleApiError(error),
            loading: false,
          });
          return false;
        }
      },

      logout: () => {
        localStorage.removeItem('admin_token');
        set({
          user: null,
          token: null,
          error: null,
        });
      },

      checkAuth: () => {
        const token = localStorage.getItem('admin_token');
        if (token) {
          set({ 
            token,
            // In real app, validate token and fetch user data
            user: {
              id: 1,
              username: 'admin',
              email: 'admin@guestbook.local',
              is_active: true,
              is_superuser: true,
              created_at: new Date().toISOString()
            }
          });
        }
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ 
        token: state.token,
        user: state.user 
      }),
    }
  )
);
