/**
 * TypeScript type definitions for auth service
 */

export interface SyncUserResponse {
  accessToken?: string;
  refreshToken?: string;
  user: {
    id: string;
    email: string;
    name: string;
  };
  needsOnboarding: boolean;
}

export interface ErrorResponse {
  error: string;
  details?: string;
}
