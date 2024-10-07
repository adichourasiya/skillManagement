import sqlite3

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('admin', 'student'))
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    score INTEGER DEFAULT 0,
                    url TEXT NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students(id)
                )''')
    conn.commit()
    conn.close()

def seed_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Check if the users table is empty
    c.execute('SELECT COUNT(*) FROM users')
    if c.fetchone()[0] == 0:
        # Insert initial admin user
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                  ('admin', 'admin_password', 'admin'))
        # Insert initial student user
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                  ('student', 'student_password', 'student'))

    # Check if the students table is empty
    c.execute('SELECT COUNT(*) FROM students')
    if c.fetchone()[0] == 0:
        # Insert initial students
        c.execute("INSERT INTO students (name) VALUES (?)", ('Student A',))
        c.execute("INSERT INTO students (name) VALUES (?)", ('Student B',))

    # Check if the skills table is empty
    c.execute('SELECT COUNT(*) FROM skills')
    if c.fetchone()[0] == 0:
        # Insert initial skills for the first student
        c.execute("INSERT INTO skills (student_id, name, url) VALUES (?, ?, ?)", 
                  (1, 'Math', 'http://example.com/math'))
        c.execute("INSERT INTO skills (student_id, name, url) VALUES (?, ?, ?)", 
                  (1, 'Science', 'http://example.com/science'))
        # Insert initial skills for the second student
        c.execute("INSERT INTO skills (student_id, name, url) VALUES (?, ?, ?)", 
                  (2, 'English', 'http://example.com/english'))

    conn.commit()
    conn.close()
    print("Database seeded successfully.")

if __name__ == '__main__':
    init_db()  # Initialize the database
    seed_db()  # Seed the database with initial data
