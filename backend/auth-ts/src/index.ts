/**
 * Express server entry point for Better Auth service
 * Handles authentication via email/password and Google OAuth
 */

// Load env vars FIRST before any other imports
import dotenv from "dotenv";
dotenv.config();

import express from "express";
import cors from "cors";
import { toNodeHandler } from "better-auth/node";
import { auth } from "./auth.js";
import { syncUserRoute } from "./routes/sync-user.js";

const app = express();
const PORT = process.env.PORT || 3001;

// CORS configuration - allow frontend and FastAPI backend
app.use(cors({
  origin: [
    process.env.FRONTEND_URL || "http://localhost:3000",
    process.env.BACKEND_URL || "http://localhost:8000",
  ],
  credentials: true, // Allow HTTP-only cookies
}));

// Request logging middleware (before auth handler)
app.use((req, _res, next) => {
  console.log(`${req.method} ${req.url}`);
  next();
});

// NOTE: Google OAuth is now initiated client-side via authClient.signIn.social("google")
// This properly sets the state cookie in the browser before redirecting.
// The custom /api/auth/google route is removed to prevent state_mismatch errors.

// Better Auth handler - handles all /api/auth/* routes
// IMPORTANT: Must be BEFORE express.json() middleware
app.all("/api/auth/*", toNodeHandler(auth));

// Parse JSON bodies - AFTER Better Auth handler
// (express.json() before auth handler breaks better-auth)
app.use(express.json());

// Custom routes
app.use("/api", syncUserRoute);

// Health check endpoint
app.get("/health", (_req, res) => {
  res.json({
    status: "ok",
    service: "auth-ts",
    timestamp: new Date().toISOString()
  });
});

// 404 handler
app.use((_req, res) => {
  res.status(404).json({ error: "Not found" });
});

// Error handler
app.use((err: Error, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
  console.error("❌ Server error:", err);
  res.status(500).json({ error: "Internal server error" });
});

// Start server
app.listen(PORT, () => {
  console.log(`\n🚀 Auth service running on port ${PORT}`);
  console.log(`📍 Base URL: ${process.env.AUTH_SERVICE_URL || `http://localhost:${PORT}`}`);
  console.log(`🔐 Email/password auth: ENABLED`);
  console.log(`🔗 Google OAuth: ${process.env.GOOGLE_CLIENT_ID ? 'ENABLED' : 'DISABLED (missing credentials)'}`);
  console.log(`\nEndpoints:`);
  console.log(`  POST /api/auth/sign-up/email - Email/password signup`);
  console.log(`  POST /api/auth/sign-in/email - Email/password login`);
  console.log(`  POST /api/auth/sign-in/social - Social OAuth (Google)`);
  console.log(`  GET  /api/auth/callback/google - Google OAuth callback`);
  console.log(`  POST /api/sync-user - Sync user & get JWT tokens\n`);
});
