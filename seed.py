import psycopg
from psycopg.rows import dict_row

def init_db(database_url):
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE
                )
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('admin', 'student')),
                    student_id INTEGER REFERENCES students(id)
                )
            ''')
            cur.execute('''
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS student_id INTEGER REFERENCES students(id)
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS skills (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
                    name TEXT NOT NULL,
                    score INTEGER DEFAULT 0,
                    url TEXT NOT NULL
                )
            ''')
            cur.execute('''
                CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_skill
                ON skills (student_id, name, url)
            ''')
        conn.commit()

def seed_db(database_url):
    with psycopg.connect(database_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO students (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                ('Student A',)
            )
            cur.execute(
                "INSERT INTO students (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                ('Student B',)
            )
            student_a = cur.execute(
                "SELECT id FROM students WHERE name=%s",
                ('Student A',)
            ).fetchone()['id']
            student_b = cur.execute(
                "SELECT id FROM students WHERE name=%s",
                ('Student B',)
            ).fetchone()['id']

            cur.execute(
                "INSERT INTO users (username, password, role, student_id) VALUES (%s, %s, %s, %s) "
                "ON CONFLICT (username) DO NOTHING",
                ('admin', 'admin_password', 'admin', None)
            )
            cur.execute(
                "INSERT INTO users (username, password, role, student_id) VALUES (%s, %s, %s, %s) "
                "ON CONFLICT (username) DO UPDATE SET student_id = EXCLUDED.student_id",
                ('student', 'student_password', 'student', student_a)
            )

            cur.execute(
                "INSERT INTO skills (student_id, name, url) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                (student_a, 'Math', 'http://example.com/math')
            )
            cur.execute(
                "INSERT INTO skills (student_id, name, url) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                (student_a, 'Science', 'http://example.com/science')
            )
            cur.execute(
                "INSERT INTO skills (student_id, name, url) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                (student_b, 'English', 'http://example.com/english')
            )
        conn.commit()
    print("Database seeded successfully.")

if __name__ == '__main__':
    import os

    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise RuntimeError('DATABASE_URL is required to run seed.py directly.')
    init_db(database_url)
    seed_db(database_url)
