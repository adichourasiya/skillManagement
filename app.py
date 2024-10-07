from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database (SQLite) if it doesn't exist
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            score INTEGER DEFAULT 0,
            url TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    ''')
    conn.commit()
    conn.close()

# Home route (admin view by default)
@app.route('/')
def admin_dashboard():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Fetch all students for the admin dashboard
    c.execute('SELECT * FROM students')
    students = c.fetchall()

    conn.close()
    return render_template('admin_dashboard.html', students=students)

# Route for adding a student
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['student_name']
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO students (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('admin_dashboard'))

# Route for removing a student
@app.route('/remove_student', methods=['POST'])
def remove_student():
    student_id = request.form['student_id']
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('DELETE FROM students WHERE id=?', (student_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('admin_dashboard'))

# Route for adding a skill to a student
@app.route('/add_skill', methods=['POST'])
def add_skill():
    student_id = request.form['student_id']
    skill_name = request.form['skill_name']
    skill_url = request.form['skill_url']
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO skills (student_id, name, url) VALUES (?, ?, ?)', (student_id, skill_name, skill_url))
    conn.commit()
    conn.close()
    
    return redirect(url_for('admin_dashboard'))

# Route for removing a skill from a student
@app.route('/remove_skill', methods=['POST'])
def remove_skill():
    student_id = request.form['student_id']
    skill_name = request.form['skill_name']
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('DELETE FROM skills WHERE student_id=? AND name=?', (student_id, skill_name))
    conn.commit()
    conn.close()
    
    return redirect(url_for('admin_dashboard'))

# Route for the student dashboard (students see their skills)
@app.route('/student/<int:student_id>')
def student_dashboard(student_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Fetch student's skills
    c.execute('SELECT name, score, url FROM skills WHERE student_id=?', (student_id,))
    skills = c.fetchall()

    conn.close()
    return render_template('student_dashboard.html', skills=skills)

if __name__ == '__main__':
    init_db()  # Initialize the database when starting the app
    app.run(debug=True)
