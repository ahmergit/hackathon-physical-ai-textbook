/**
 * Better Auth React client
 * Connects to the TypeScript auth service for authentication
 */

import { createAuthClient } from "better-auth/react";

// Get auth service URL - use localhost for development
// In production, this should be configured via build-time environment variables
const authServiceUrl =
  typeof process !== 'undefined' && process.env?.AUTH_SERVICE_URL
    ? process.env.AUTH_SERVICE_URL
    : "http://localhost:3001";

export const authClient = createAuthClient({
  baseURL: authServiceUrl,
  // credentials: "include", // Send HTTP-only cookies
});

// Export commonly used hooks and functions
export const {
  signIn,
  signUp,
  signOut,
  useSession,
  $Infer,
} = authClient;

// Type inference for session data
export type Session = typeof $Infer.Session.session;
export type User = typeof $Infer.Session.user;
