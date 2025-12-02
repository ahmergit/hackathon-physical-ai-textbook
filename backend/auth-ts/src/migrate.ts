/**
 * Manual migration script for better-auth tables
 * Run with: npx tsx src/migrate.ts
 */

import { Pool } from "pg";
import dotenv from "dotenv";

dotenv.config();

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false,
  },
});

const createTables = async () => {
  const client = await pool.connect();
  
  try {
    console.log("🔄 Creating better-auth tables...");
    
    // Create user table
    await client.query(`
      CREATE TABLE IF NOT EXISTS "user" (
        "id" TEXT PRIMARY KEY,
        "name" TEXT NOT NULL,
        "email" TEXT UNIQUE NOT NULL,
        "emailVerified" BOOLEAN DEFAULT FALSE,
        "image" TEXT,
        "createdAt" TIMESTAMP DEFAULT NOW(),
        "updatedAt" TIMESTAMP DEFAULT NOW()
      );
    `);
    console.log("✅ Created 'user' table");

    // Create session table
    await client.query(`
      CREATE TABLE IF NOT EXISTS "session" (
        "id" TEXT PRIMARY KEY,
        "expiresAt" TIMESTAMP NOT NULL,
        "token" TEXT UNIQUE NOT NULL,
        "createdAt" TIMESTAMP DEFAULT NOW(),
        "updatedAt" TIMESTAMP DEFAULT NOW(),
        "ipAddress" TEXT,
        "userAgent" TEXT,
        "userId" TEXT NOT NULL REFERENCES "user"("id") ON DELETE CASCADE
      );
    `);
    console.log("✅ Created 'session' table");

    // Create account table
    await client.query(`
      CREATE TABLE IF NOT EXISTS "account" (
        "id" TEXT PRIMARY KEY,
        "accountId" TEXT NOT NULL,
        "providerId" TEXT NOT NULL,
        "userId" TEXT NOT NULL REFERENCES "user"("id") ON DELETE CASCADE,
        "accessToken" TEXT,
        "refreshToken" TEXT,
        "idToken" TEXT,
        "accessTokenExpiresAt" TIMESTAMP,
        "refreshTokenExpiresAt" TIMESTAMP,
        "scope" TEXT,
        "password" TEXT,
        "createdAt" TIMESTAMP DEFAULT NOW(),
        "updatedAt" TIMESTAMP DEFAULT NOW()
      );
    `);
    console.log("✅ Created 'account' table");

    // Create verification table
    await client.query(`
      CREATE TABLE IF NOT EXISTS "verification" (
        "id" TEXT PRIMARY KEY,
        "identifier" TEXT NOT NULL,
        "value" TEXT NOT NULL,
        "expiresAt" TIMESTAMP NOT NULL,
        "createdAt" TIMESTAMP DEFAULT NOW(),
        "updatedAt" TIMESTAMP DEFAULT NOW()
      );
    `);
    console.log("✅ Created 'verification' table");

    // Create jwks table
    await client.query(`
      CREATE TABLE IF NOT EXISTS "jwks" (
        "id" TEXT PRIMARY KEY,
        "publicKey" TEXT NOT NULL,
        "privateKey" TEXT NOT NULL,
        "createdAt" TIMESTAMP DEFAULT NOW(),
        "expiresAt" TIMESTAMP
      );
    `);
    console.log("✅ Created 'jwks' table");

    console.log("\n🎉 All tables created successfully!");
    
  } catch (error) {
    console.error("❌ Migration error:", error);
    throw error;
  } finally {
    client.release();
    await pool.end();
  }
};

createTables().catch(console.error);
