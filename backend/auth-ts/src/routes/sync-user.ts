/**
 * User sync route - bridges Better Auth and FastAPI
 *
 * After successful authentication (email/password OR Google OAuth),
 * this endpoint:
 * 1. Verifies Better Auth session
 * 2. Syncs user to legacy `users` table (for FastAPI compatibility)
 * 3. Generates JWT tokens for FastAPI API access
 * 4. Returns tokens + onboarding status
 */

import { Router, Request, Response } from "express";
import { v4 as uuidv4 } from "uuid";
import jwt from "jsonwebtoken";
import { auth } from "../auth.js";
import pool from "../db.js";
import type { SyncUserResponse, ErrorResponse } from "../types/index.js";

// JWT configuration - MUST match FastAPI jwt_secret
const JWT_SECRET = process.env.JWT_SECRET || "your-secret-key-change-in-production";
const ACCESS_TOKEN_EXPIRY = "1h";  // 1 hour
const REFRESH_TOKEN_EXPIRY = "7d"; // 7 days

/**
 * Generate JWT access token for FastAPI authentication
 */
function generateAccessToken(userId: string, email: string): string {
  return jwt.sign(
    { 
      userId, 
      sub: userId,  // Standard JWT claim
      email,
      type: "access"
    },
    JWT_SECRET,
    { expiresIn: ACCESS_TOKEN_EXPIRY }
  );
}

/**
 * Generate JWT refresh token
 */
function generateRefreshToken(userId: string): string {
  return jwt.sign(
    { 
      userId,
      sub: userId,
      type: "refresh"
    },
    JWT_SECRET,
    { expiresIn: REFRESH_TOKEN_EXPIRY }
  );
}

export const syncUserRoute = Router();

syncUserRoute.post("/sync-user", async (req: Request, res: Response<SyncUserResponse | ErrorResponse>) => {
  try {
    // Get session from Better Auth (from HTTP-only cookie)
    const session = await auth.api.getSession({
      headers: req.headers as any
    });

    if (!session || !session.user) {
      return res.status(401).json({ error: "Not authenticated" });
    }

    const betterAuthUserId = session.user.id;
    const userEmail = session.user.email;
    const userName = session.user.name;

    console.log(`📝 Syncing user: ${userEmail} (better-auth ID: ${betterAuthUserId})`);

    // Check if user already exists in legacy users table by email
    const existingUser = await pool.query(
      "SELECT id FROM users WHERE email = $1",
      [userEmail]
    );

    let fastApiUserId: string;

    if (existingUser.rows.length > 0) {
      // User exists, use their existing UUID
      fastApiUserId = existingUser.rows[0].id;
      console.log(`✅ Found existing user in legacy table: ${fastApiUserId}`);
      
      // Update user info
      await pool.query(
        `UPDATE users SET name = $1, is_verified = true, updated_at = NOW() WHERE id = $2`,
        [userName, fastApiUserId]
      );
    } else {
      // Create new user with a proper UUID
      fastApiUserId = uuidv4();
      console.log(`📝 Creating new user in legacy table: ${fastApiUserId}`);
      
      await pool.query(
        `INSERT INTO users (id, email, hashed_password, is_active, is_superuser, is_verified, name, created_at, updated_at)
         VALUES ($1, $2, '', true, false, true, $3, NOW(), NOW())`,
        [fastApiUserId, userEmail, userName]
      );
    }

    console.log(`✅ User synced to legacy users table`);

    // Check if profile exists (determines if onboarding needed)
    const profileResult = await pool.query(
      "SELECT id FROM profiles WHERE user_id = $1",
      [fastApiUserId]
    );

    const hasProfile = profileResult.rows.length > 0;

    // Generate JWT tokens for FastAPI API access
    const accessToken = generateAccessToken(fastApiUserId, userEmail);
    const refreshToken = generateRefreshToken(fastApiUserId);

    console.log(`🔑 Generated JWT tokens for user: ${fastApiUserId}`);

    return res.json({
      user: {
        id: fastApiUserId,
        email: userEmail,
        name: userName,
      },
      accessToken,
      refreshToken,
      needsOnboarding: !hasProfile,
    });

  } catch (error) {
    console.error("❌ Error syncing user:", error);
    return res.status(500).json({
      error: "Internal server error",
      details: error instanceof Error ? error.message : String(error)
    });
  }
});
