/**
 * Better Auth configuration
 * Enables email/password (primary) and Google OAuth (secondary) authentication
 */

import { betterAuth } from "better-auth";
import { v4 as uuidv4 } from "uuid";
import pool from "./db.js";

export const auth = betterAuth({
  database: pool,
  baseURL: process.env.BETTER_AUTH_URL || process.env.AUTH_SERVICE_URL || "http://localhost:3001",
  basePath: "/api/auth",
  trustedOrigins: [
    process.env.FRONTEND_URL || "http://localhost:3000",
    process.env.BACKEND_URL || "http://localhost:8000",
    "http://localhost:3001",
  ],

  // Advanced configuration for OAuth state handling and UUID generation
  advanced: {
    crossSubDomainCookies: {
      enabled: false,
    },
    cookiePrefix: "better-auth",
    useSecureCookies: false, // Set to true in production with HTTPS
    generateId: () => uuidv4(), // Generate UUIDs for compatibility with FastAPI
    // Fix state_mismatch: Configure OAuth state cookie for proper cross-site handling
    cookies: {
      oauth_state: {
        name: "better-auth.oauth_state",
        options: {
          sameSite: "lax" as const,
          secure: false, // Set to true in production with HTTPS
          path: "/",
          httpOnly: true,
          maxAge: 60 * 10, // 10 minutes
        },
      },
    },
  },

  // ENABLE email/password authentication (PRIMARY METHOD)
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Set to true if email verification needed
    minPasswordLength: 8,
    maxPasswordLength: 128,
  },

  // Enable Google OAuth (SECONDARY OPTION)
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },

  session: {
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60 * 1000, // 5 minutes
    },
  },

  // User model configuration - name is already a default field in better-auth
  // No need to add it as additionalField
});

export type Session = typeof auth.$Infer.Session.session;
export type User = typeof auth.$Infer.Session.user;
