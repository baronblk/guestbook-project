import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { adminApi, apiUtils } from '../api';
import { AdminUser, AuthStore, LoginForm } from '../types';

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

      checkAuth: async () => {
        const token = localStorage.getItem('admin_token');
        if (token) {
          try {
            // Validierung durch einen API-Call zum Backend
            await adminApi.getReviews({ page: 1, per_page: 1 });
            set({
              token,
              user: {
                id: 1,
                username: 'admin',
                email: 'admin@guestbook.local',
                is_active: true,
                is_superuser: true,
                created_at: new Date().toISOString()
              }
            });
          } catch (error: any) {
            // Token ist ungültig oder Session abgelaufen
            if (error.response?.status === 401 || error.response?.status === 403) {
              localStorage.removeItem('admin_token');
              set({ token: null, user: null });
            }
          }
        }
      },

      // Neue Funktion für kontinuierliche Session-Überwachung
      validateSession: async () => {
        const token = get().token;
        if (!token) return false;

        try {
          await adminApi.getReviews({ page: 1, per_page: 1 });
          return true;
        } catch (error: any) {
          if (error.response?.status === 401 || error.response?.status === 403) {
            get().logout();
            return false;
          }
          return true; // Anderer Fehler, Session könnte noch gültig sein
        }
      },

      // Session verlängern/refreshen
      refreshSession: async () => {
        const currentToken = get().token;
        if (!currentToken) return false;

        try {
          const tokenResponse = await adminApi.refreshToken();

          // Store new token
          localStorage.setItem('admin_token', tokenResponse.access_token);

          set({
            token: tokenResponse.access_token,
            user: get().user, // Benutzer bleibt gleich
          });

          return true;
        } catch (error: any) {
          // Token refresh fehlgeschlagen - logout
          if (error.response?.status === 401 || error.response?.status === 403) {
            get().logout();
          }
          return false;
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
