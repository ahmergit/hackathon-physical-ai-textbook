/**
 * API client for FastAPI backend.
 * Updated for Better Auth JWT authentication.
 *
 * Authentication handled by Better Auth TypeScript service.
 * This client adds Bearer tokens to requests for protected FastAPI routes.
 */

import axios, { AxiosInstance, AxiosError } from 'axios';

// API base URLs - browser-compatible environment variable access
const API_BASE_URL =
  typeof process !== 'undefined' && process.env?.BACKEND_URL
    ? process.env.BACKEND_URL
    : 'http://localhost:8000';
const AUTH_SERVICE_URL =
  typeof process !== 'undefined' && process.env?.AUTH_SERVICE_URL
    ? process.env.AUTH_SERVICE_URL
    : 'http://localhost:3001';
const API_TIMEOUT = 30000;

/**
 * Enums matching backend models
 */
export enum SkillLevel {
  BEGINNER = 'beginner',
  INTERMEDIATE = 'intermediate',
  EXPERT = 'expert',
}

export enum DeviceType {
  CLOUD_LAPTOP = 'cloud_laptop',
  RTX_GPU = 'rtx_gpu',
  PHYSICAL_ROBOT = 'physical_robot',
}

/**
 * Axios instance configured for FastAPI backend.
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Request interceptor: Add Bearer token from localStorage
 */
apiClient.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

/**
 * Response interceptor: Handle 401 with token refresh
 */
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as any;

    // Handle 401 Unauthorized - try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      // Check if we have tokens to refresh
      const refreshToken = localStorage.getItem('refresh_token');
      const accessToken = localStorage.getItem('access_token');
      
      // If no tokens exist, just reject without redirect
      // This happens during initial login/onboarding flow
      if (!refreshToken && !accessToken) {
        return Promise.reject(error);
      }

      try {
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        const response = await axios.post(
          `${AUTH_SERVICE_URL}/api/auth/refresh`,
          { refreshToken }
        );

        const { accessToken: newAccessToken } = response.data;
        localStorage.setItem('access_token', newAccessToken);

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return axios.request(originalRequest);

      } catch (refreshError) {
        // Refresh failed - clear tokens
        console.error('Token refresh failed:', refreshError);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');

        // Only redirect if we actually had tokens (real session expiry)
        // Don't redirect during initial auth flow
        if (accessToken || refreshToken) {
          if (typeof window !== 'undefined') {
            window.dispatchEvent(new CustomEvent('auth:unauthorized'));
            // Don't redirect from onboarding page - let it handle the error
            if (!window.location.pathname.includes('/onboarding')) {
              window.location.href = '/physical-ai-humaniod-robotics/?error=session_expired';
            }
          }
        }

        return Promise.reject(refreshError);
      }
    }

    // Handle other errors
    if (error.response) {
      const { status } = error.response;

      if (status === 403) {
        console.warn('Forbidden access');
      }

      if (status === 422) {
        console.error('Validation error:', error.response.data);
      }
    } else if (error.request) {
      console.error('No response from server:', error.message);
    } else {
      console.error('Request error:', error.message);
    }

    return Promise.reject(error);
  }
);

/**
 * Profile API methods (Protected routes - require JWT)
 */
export const profileAPI = {
  /**
   * Get current user's profile
   */
  async getProfile() {
    const response = await apiClient.get('/api/profile');
    return response.data;
  },

  /**
   * Create user profile (onboarding)
   */
  async createProfile(data: {
    hardware_skill: 'beginner' | 'intermediate' | 'expert';
    programming_skill: 'beginner' | 'intermediate' | 'expert';
    ai_ml_skill: 'beginner' | 'intermediate' | 'expert';
    current_device: 'cloud_laptop' | 'rtx_gpu' | 'physical_robot';
  }) {
    const response = await apiClient.post('/api/profile', data);
    return response.data;
  },

  /**
   * Update user profile
   */
  async updateProfile(data: Partial<{
    hardware_skill: 'beginner' | 'intermediate' | 'expert';
    programming_skill: 'beginner' | 'intermediate' | 'expert';
    ai_ml_skill: 'beginner' | 'intermediate' | 'expert';
    current_device: 'cloud_laptop' | 'rtx_gpu' | 'physical_robot';
  }>) {
    const response = await apiClient.put('/api/profile', data);
    return response.data;
  },

  /**
   * Delete user profile
   */
  async deleteProfile() {
    await apiClient.delete('/api/profile');
  },
};

/**
 * Chat API methods (Protected routes - require JWT)
 */
export const chatAPI = {
  /**
   * Send chat message (SSE streaming handled separately)
   */
  async sendMessage(message: string, conversationHistory?: any[]) {
    const response = await apiClient.post('/api/chat', {
      query: message,
      conversation_history: conversationHistory || [],
    });
    return response.data;
  },

  /**
   * Health check
   */
  async healthCheck() {
    const response = await apiClient.get('/api/chat/health');
    return response.data;
  },
};

/**
 * Export the configured axios instance for custom requests
 */
export default apiClient;
