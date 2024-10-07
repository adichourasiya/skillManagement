from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username, password = request.form['username'], request.form['password']
    with get_db_connection() as conn:
        user = conn.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password)).fetchone()

    if user:
        session.update(username=username, role=user['role'])
        return redirect(url_for('dashboard'))
    return "Invalid username or password"

@app.route('/dashboard')
def dashboard():
    if 'role' not in session:
        return redirect(url_for('home'))
    return redirect(url_for('admin_dashboard')) if session['role'] == 'admin' else redirect(url_for('student_dashboard', student_id=session['student_id']))

@app.route('/admin_dashboard')
def admin_dashboard():
    with get_db_connection() as conn:
        students = conn.execute('SELECT * FROM students').fetchall()
    return render_template('admin_dashboard.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['student_name']
    with get_db_connection() as conn:
        conn.execute('INSERT INTO students (name) VALUES (?)', (name,))
        conn.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/remove_student', methods=['POST'])
def remove_student():
    student_id = request.form['student_id']
    with get_db_connection() as conn:
        conn.execute('DELETE FROM students WHERE id=?', (student_id,))
        conn.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/add_skill', methods=['POST'])
def add_skill():
    student_id, skill_name, skill_url = request.form['student_id'], request.form['skill_name'], request.form['skill_url']
    with get_db_connection() as conn:
        conn.execute('INSERT INTO skills (student_id, name, url) VALUES (?, ?, ?)', (student_id, skill_name, skill_url))
        conn.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/remove_skill', methods=['POST'])
def remove_skill():
    student_id, skill_name = request.form['student_id'], request.form['skill_name']
    with get_db_connection() as conn:
        conn.execute('DELETE FROM skills WHERE student_id=? AND name=?', (student_id, skill_name))
        conn.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/student/<int:student_id>')
def student_dashboard(student_id):
    with get_db_connection() as conn:
        skills = conn.execute('SELECT name, score, url FROM skills WHERE student_id=?', (student_id,)).fetchall()
    return render_template('student_dashboard.html', skills=skills)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)