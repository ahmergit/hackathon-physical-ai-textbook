/**
 * AuthContext - Updated for Better Auth integration
 *
 * Handles authentication flow:
 * 1. Better Auth manages email/password + Google OAuth
 * 2. After auth, calls /api/sync-user to get JWT tokens
 * 3. Stores tokens in localStorage for FastAPI API calls
 * 4. Redirects to /onboarding if profile doesn't exist
 */

import React, { createContext, useContext, useState, useEffect, useRef, ReactNode } from 'react';
import { useSession, signIn, signUp, signOut } from '../lib/auth-client';
import axios from 'axios';

// Helper to get auth service URL (browser-compatible)
const getAuthServiceUrl = () =>
  typeof process !== 'undefined' && process.env?.AUTH_SERVICE_URL
    ? process.env.AUTH_SERVICE_URL
    : 'http://localhost:3001';

// Module-level sync tracking to prevent duplicate calls across StrictMode remounts
let globalSyncPromise: Promise<any> | null = null;
let globalSyncedUserId: string | null = null;

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  accessToken: string | null;

  // Email/password auth (PRIMARY)
  loginWithEmail: (email: string, password: string) => Promise<void>;
  signupWithEmail: (name: string, email: string, password: string) => Promise<void>;

  // Google OAuth (SECONDARY)
  loginWithGoogle: () => Promise<void>;

  // Common
  logout: () => Promise<void>;
  refreshAccessToken: () => Promise<string | null>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const { data: session, isPending } = useSession();
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  
  // Use ref to track synced user ID - survives re-renders
  const syncedUserIdRef = useRef<string | null>(null);

  // Sync user from Better Auth session
  useEffect(() => {
    const syncUser = async () => {
      // Skip if still pending
      if (isPending) return;
      
      if (session?.user) {
        // Skip if we already synced this user (check both ref and global)
        if (syncedUserIdRef.current === session.user.id || globalSyncedUserId === session.user.id) {
          setIsLoading(false);
          return;
        }
        
        // If there's already a sync in progress for this user, wait for it
        if (globalSyncPromise && globalSyncedUserId === session.user.id) {
          try {
            const result = await globalSyncPromise;
            setUser(result.user);
            setAccessToken(result.accessToken);
            syncedUserIdRef.current = session.user.id;
          } catch (e) {
            // Ignore - the original call will handle errors
          }
          setIsLoading(false);
          return;
        }
        
        // Start sync and store promise globally to dedupe concurrent calls
        const doSync = async () => {
          const response = await axios.post(
            `${getAuthServiceUrl()}/api/sync-user`,
            {},
            { withCredentials: true }
          );
          return response.data;
        };
        
        globalSyncPromise = doSync();
        globalSyncedUserId = session.user.id;
        
        try {
          const { user: userData, accessToken: token, refreshToken, needsOnboarding } = await globalSyncPromise;

          // Store JWT tokens for FastAPI API calls
          if (token) {
            localStorage.setItem('access_token', token);
            setAccessToken(token);
          }
          if (refreshToken) {
            localStorage.setItem('refresh_token', refreshToken);
          }

          setUser(userData);
          syncedUserIdRef.current = session.user.id;

          // Redirect to onboarding if needed (only if not already there)
          if (needsOnboarding && typeof window !== 'undefined') {
            const currentPath = window.location.pathname;
            if (!currentPath.includes('/onboarding')) {
              window.location.href = '/physical-ai-humaniod-robotics/onboarding';
            }
          }
        } catch (error) {
          console.error('Failed to sync user:', error);
          syncedUserIdRef.current = session.user.id;
        } finally {
          globalSyncPromise = null;
        }
      } else {
        // No session, clear local state
        setUser(null);
        setAccessToken(null);
        syncedUserIdRef.current = null;
        globalSyncedUserId = null;
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
      setIsLoading(false);
    };

    syncUser();
  }, [session?.user?.id, isPending]);

  // Email/password signup (PRIMARY METHOD)
  const signupWithEmail = async (name: string, email: string, password: string) => {
    try {
      await signUp.email({
        name,
        email,
        password,
      });

      // After signup, sign in automatically
      await loginWithEmail(email, password);
    } catch (error: any) {
      console.error('Signup failed:', error);
      throw new Error(error.message || 'Signup failed');
    }
  };

  // Email/password login (PRIMARY METHOD)
  const loginWithEmail = async (email: string, password: string) => {
    try {
      await signIn.email({
        email,
        password,
      });

      // Session will update automatically, triggering useEffect above
    } catch (error: any) {
      console.error('Login failed:', error);
      throw new Error(error.message || 'Login failed');
    }
  };

  // Google OAuth login (SECONDARY OPTION)
  // Uses Better Auth client to properly set state cookie before redirect
  const loginWithGoogle = async () => {
    try {
      await signIn.social({
        provider: "google",
        // Redirect to home page - AuthContext will handle sync and redirect to onboarding if needed
        callbackURL: window.location.origin + "/physical-ai-humaniod-robotics/",
      });
    } catch (error: any) {
      console.error('Google OAuth failed:', error);
      throw new Error(error.message || 'Google OAuth failed');
    }
  };

  // Logout
  const logout = async () => {
    try {
      await signOut();
      setUser(null);
      setAccessToken(null);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      if (typeof window !== 'undefined') {
        window.location.href = '/physical-ai-humaniod-robotics/';
      }
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  // Refresh access token
  const refreshAccessToken = async (): Promise<string | null> => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) return null;

      const response = await axios.post(
        `${getAuthServiceUrl()}/api/auth/refresh`,
        { refreshToken }
      );

      const { accessToken: newAccessToken } = response.data;
      localStorage.setItem('access_token', newAccessToken);
      setAccessToken(newAccessToken);
      return newAccessToken;
    } catch (error) {
      console.error('Token refresh failed:', error);
      return null;
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading: isLoading || isPending,
        accessToken,
        loginWithEmail,
        signupWithEmail,
        loginWithGoogle,
        logout,
        refreshAccessToken,
      }}
    >
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
