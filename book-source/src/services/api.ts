/**
 * API client for Physical AI Auth backend.
 * Handles all HTTP requests with axios.
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  User,
  UserProfile,
  RegisterRequest,
  RegisterResponse,
  LoginRequest,
  LoginResponse,
  VerifyEmailRequest,
  VerifyEmailResponse,
  ResendVerificationRequest,
  CreateProfileRequest,
  ForgotPasswordRequest,
  ResetPasswordRequest,
  APIError,
} from '../types/auth';

// Re-export ExperienceLevel for convenience
export { ExperienceLevel } from '../types/auth';

// API base URL - hardcoded for browser compatibility
// In production, update this or use Docusaurus customFields
const API_BASE_URL = 'http://localhost:8000';
const API_TIMEOUT = 30000;

/**
 * Axios instance configured for auth API.
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Send HTTP-only cookies
});

/**
 * Request interceptor to add auth token if available.
 */
apiClient.interceptors.request.use(
  (config) => {
    // Token is sent via HTTP-only cookie, no need to add manually
    return config;
  },
  (error) => Promise.reject(error)
);

/**
 * Response interceptor to handle errors consistently.
 */
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<APIError>) => {
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;

      if (status === 401) {
        // Unauthorized - clear auth state and redirect to login
        console.warn('Unauthorized request, clearing auth state');
        // Dispatch custom event for auth context to handle
        window.dispatchEvent(new CustomEvent('auth:unauthorized'));
      }

      if (status === 403) {
        console.warn('Forbidden access');
      }

      if (status === 422) {
        // Validation error from FastAPI
        console.error('Validation error:', data.detail);
      }
    } else if (error.request) {
      // Request made but no response
      console.error('No response from server:', error.message);
    } else {
      // Error setting up request
      console.error('Request error:', error.message);
    }

    return Promise.reject(error);
  }
);

/**
 * Authentication API methods.
 */
export const authAPI = {
  /**
   * Register a new user with email and password.
   */
  async register(data: RegisterRequest): Promise<RegisterResponse> {
    const response = await apiClient.post<RegisterResponse>('/auth/register', data);
    return response.data;
  },

  /**
   * Login with email and password.
   * Returns access token (also sets HTTP-only cookie).
   */
  async login(data: LoginRequest): Promise<LoginResponse> {
    // FastAPI expects form data for OAuth2PasswordRequestForm
    const formData = new URLSearchParams();
    formData.append('username', data.username);
    formData.append('password', data.password);

    const response = await apiClient.post<LoginResponse>('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return response.data;
  },

  /**
   * Logout current user and invalidate tokens.
   */
  async logout(): Promise<void> {
    await apiClient.post('/auth/logout');
  },

  /**
   * Get current authenticated user.
   */
  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },

  /**
   * Verify email with token from verification email.
   */
  async verifyEmail(data: VerifyEmailRequest): Promise<VerifyEmailResponse> {
    const response = await apiClient.post<VerifyEmailResponse>('/auth/verify', data);
    return response.data;
  },

  /**
   * Verify email with 6-digit verification code.
   */
  async verifyCode(data: { email: string; code: string }): Promise<VerifyEmailResponse> {
    const response = await apiClient.post<VerifyEmailResponse>('/auth/verify-code', data);
    return response.data;
  },

  /**
   * Resend verification email.
   */
  async resendVerification(data: ResendVerificationRequest): Promise<{ message: string }> {
    const response = await apiClient.post<{ message: string }>('/auth/resend-verification', data);
    return response.data;
  },

  /**
   * Request password reset email.
   */
  async forgotPassword(data: ForgotPasswordRequest): Promise<{ message: string }> {
    const response = await apiClient.post<{ message: string }>('/auth/forgot-password', data);
    return response.data;
  },

  /**
   * Reset password with token.
   */
  async resetPassword(data: ResetPasswordRequest): Promise<{ message: string }> {
    const response = await apiClient.post<{ message: string }>('/auth/reset-password', data);
    return response.data;
  },

  /**
   * Initiate Google OAuth flow.
   * Returns authorization URL to redirect to.
   */
  getGoogleAuthURL(): string {
    return `${API_BASE_URL}/auth/google`;
  },
};

/**
 * Profile API methods.
 */
export const profileAPI = {
  /**
   * Get current user's profile.
   */
  async getProfile(): Promise<UserProfile> {
    const response = await apiClient.get<UserProfile>('/profile');
    return response.data;
  },

  /**
   * Create user profile (onboarding).
   */
  async createProfile(data: CreateProfileRequest): Promise<UserProfile> {
    const response = await apiClient.post<UserProfile>('/profile', data);
    return response.data;
  },

  /**
   * Update existing user profile.
   */
  async updateProfile(data: Partial<CreateProfileRequest>): Promise<UserProfile> {
    const response = await apiClient.put<UserProfile>('/profile', data);
    return response.data;
  },
};

/**
 * Health check API.
 */
export const healthAPI = {
  /**
   * Check API health status.
   */
  async checkHealth(): Promise<{ status: string; service: string; version: string }> {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

/**
 * Export configured axios instance for advanced use cases.
 */
export { apiClient };

/**
 * Export default API object with all methods.
 */
export default {
  auth: authAPI,
  profile: profileAPI,
  health: healthAPI,
};
