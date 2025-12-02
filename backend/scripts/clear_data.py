"""
Clear all data from the database tables.
"""

import psycopg2

DB_URL = "postgresql://neondb_owner:npg_jLEJ7HAvlF4r@ep-patient-mode-a1bof06j-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

# Delete all data from tables (in correct order due to foreign keys)
tables_to_clear = ['profiles', 'session', 'account', 'users', 'user']

print('🗑️  Clearing all data from tables...')
for table in tables_to_clear:
    try:
        cur.execute(f'DELETE FROM "{table}"')
        count = cur.rowcount
        print(f'  ✅ Deleted {count} rows from: {table}')
    except Exception as e:
        print(f'  ❌ Error clearing {table}: {e}')

conn.commit()
print('\n✅ All data cleared!')

cur.close()
conn.close()
