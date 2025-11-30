/**
 * useAuth hook for authentication state management
 */

import { useState, useEffect, useCallback } from 'react';
import { authAPI } from '../services/api';
import type { User } from '../types/auth';

interface UseAuthReturn {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  error: string | null;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

export function useAuth(): UseAuthReturn {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchUser = useCallback(async () => {
    try {
      const currentUser = await authAPI.getCurrentUser();
      setUser(currentUser);
      setError(null);
    } catch (err: any) {
      if (err.response?.status === 401) {
        // Not authenticated, clear user state
        setUser(null);
      } else {
        setError('Failed to fetch user data');
      }
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      await authAPI.logout();
      setUser(null);
      setError(null);
      // Redirect to home page
      window.location.href = '/physical-ai-humaniod-robotics/';
    } catch (err: any) {
      setError('Logout failed');
    }
  }, []);

  const refreshUser = useCallback(async () => {
    setLoading(true);
    await fetchUser();
  }, [fetchUser]);

  useEffect(() => {
    fetchUser();

    // Listen for unauthorized events from API interceptor
    const handleUnauthorized = () => {
      setUser(null);
      setError('Session expired. Please log in again.');
    };

    window.addEventListener('auth:unauthorized', handleUnauthorized);

    return () => {
      window.removeEventListener('auth:unauthorized', handleUnauthorized);
    };
  }, [fetchUser]);

  return {
    user,
    loading,
    isAuthenticated: user !== null,
    error,
    logout,
    refreshUser,
  };
}
