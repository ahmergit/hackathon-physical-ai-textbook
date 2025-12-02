/**
 * PostgreSQL database connection pool
 * Shared with FastAPI backend via DATABASE_URL
 */

import { Pool } from "pg";
import dotenv from "dotenv";

dotenv.config();

// Create connection pool
// Neon DB requires SSL for all connections
export const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false, // Required for Neon DB
  },
  max: 10, // Smaller pool for serverless
  idleTimeoutMillis: 60000, // 60 seconds idle timeout
  connectionTimeoutMillis: 30000, // 30 seconds to connect (Neon can be slow to wake)
  keepAlive: true,
  keepAliveInitialDelayMillis: 10000,
});

// Test connection
pool.on("connect", () => {
  console.log("✅ PostgreSQL connected");
});

pool.on("error", (err) => {
  console.error("❌ PostgreSQL connection error:", err);
  process.exit(1);
});

export default pool;
