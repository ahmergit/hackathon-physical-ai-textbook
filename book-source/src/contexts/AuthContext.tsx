import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI } from '../services/api';

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const AUTH_STORAGE_KEY = 'physical_ai_auth_user';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load user from localStorage on mount AND check for OAuth callback params
  useEffect(() => {
    try {
      // Check for OAuth callback parameters in URL
      if (typeof window !== 'undefined') {
        const urlParams = new URLSearchParams(window.location.search);
        const authToken = urlParams.get('auth_token');
        const userData = urlParams.get('user');
        
        if (authToken && userData) {
          // OAuth callback - save token and user data
          localStorage.setItem('access_token', authToken);
          const parsedUser = JSON.parse(decodeURIComponent(userData));
          setUser(parsedUser);
          
          // Clean up URL params
          const cleanUrl = window.location.pathname;
          window.history.replaceState({}, document.title, cleanUrl);
          setIsLoading(false);
          return;
        }
      }
      
      // No OAuth params - load from localStorage
      const stored = localStorage.getItem(AUTH_STORAGE_KEY);
      if (stored) {
        setUser(JSON.parse(stored));
      }
    } catch (e) {
      console.error('Failed to load auth state:', e);
    }
    setIsLoading(false);
  }, []);

  // Save user to localStorage when it changes
  useEffect(() => {
    if (user) {
      localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user));
    } else {
      localStorage.removeItem(AUTH_STORAGE_KEY);
    }
  }, [user]);

  const login = async (email: string, password: string) => {
    // Use authAPI for login
    const tokenData = await authAPI.login({ username: email, password });
    
    // Store token
    localStorage.setItem('access_token', tokenData.access_token);
    
    // Get user info
    try {
      const userData = await authAPI.getCurrentUser();
      const loggedInUser: User = {
        id: userData.id,
        email: userData.email,
        name: (userData as any).name || userData.email.split('@')[0],
      };
      setUser(loggedInUser);
    } catch {
      // If getCurrentUser fails, create user from email
      const loggedInUser: User = {
        id: '',
        email: email,
        name: email.split('@')[0],
      };
      setUser(loggedInUser);
    }
  };

  const signup = async (name: string, email: string, password: string) => {
    try {
      // Use authAPI for registration with name
      const userData = await authAPI.register({
        email,
        password,
        name,
      });
      
      // Auto-login after registration (email verification disabled)
      const tokenData = await authAPI.login({ username: email, password });
      localStorage.setItem('access_token', tokenData.access_token);
      
      // Create user from response
      const newUser: User = {
        id: userData.id,
        email: userData.email,
        name: name || email.split('@')[0],
      };
      
      setUser(newUser);
      
      // Redirect to onboarding to set up profile
      window.location.href = '/physical-ai-humaniod-robotics/onboarding';
      
    } catch (error: any) {
      // Extract meaningful error message from API response
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail;
        if (typeof detail === 'string') {
          throw new Error(detail);
        } else if (detail.reason) {
          throw new Error(detail.reason);
        } else if (Array.isArray(detail)) {
          // Validation errors array
          throw new Error(detail.map((d: any) => d.msg).join(', '));
        }
      }
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    authAPI.logout().catch(() => {}); // Ignore logout errors
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
