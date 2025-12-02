"""
Cleanup unused database tables.
Removes tables not needed since email verification is disabled.
"""

import psycopg2

DB_URL = "postgresql://neondb_owner:npg_jLEJ7HAvlF4r@ep-patient-mode-a1bof06j-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

# Tables to drop (not used):
# - email_verifications: FastAPI email verification (disabled)
# - verification: Better Auth verification tokens (disabled)
# - jwks: Better Auth JWT keys (using cookie sessions)
# - oauth_accounts: FastAPI duplicate (Better Auth uses 'account' table)
tables_to_drop = ['email_verifications', 'verification', 'jwks', 'oauth_accounts']

print("🗑️  Dropping unused tables...")
for table in tables_to_drop:
    try:
        cur.execute(f'DROP TABLE IF EXISTS {table} CASCADE')
        print(f'  ✅ Dropped: {table}')
    except Exception as e:
        print(f'  ❌ Error dropping {table}: {e}')

conn.commit()

# List remaining tables
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
print('\n📋 Remaining tables (6 total expected):')
for row in cur.fetchall():
    print(f'  - {row[0]}')

cur.close()
conn.close()
print("\n✅ Cleanup complete!")
