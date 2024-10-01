from flask import Flask, render_template, request, redirect, session, url_for
import csv
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
filename = "employee_skills.csv"

# Function to load or create CSV file
def load_or_create_csv():
    file_exists = os.path.isfile(filename)
    if not file_exists:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Employee Name", "Skill", "Skill Level"])  # Headers
        print(f"Created new CSV file: {filename}")
    else:
        print(f"Loaded existing CSV file: {filename}")

# Function to add a new employee skill record
def add_employee_skill(employee_name, skill, skill_level):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([employee_name, skill, skill_level])

# Function to get all employee skills
def get_all_skills():
    if os.path.isfile(filename):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            return list(reader)
    return []

# Function to edit an employee skill record
def edit_employee_skill(old_data, new_data):
    skills = get_all_skills()
    updated_skills = [new_data if skill == old_data else skill for skill in skills]
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Employee Name", "Skill", "Skill Level"])  # Headers
        writer.writerows(updated_skills)

# Function to delete an employee skill record
def delete_employee_skill(employee_name, skill):
    skills = get_all_skills()
    updated_skills = [skill for skill in skills if not (skill[0] == employee_name and skill[1] == skill)]
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Employee Name", "Skill", "Skill Level"])  # Headers
        writer.writerows(updated_skills)

# Function to check admin credentials
def check_admin_credentials(username, password):
    return username == 'admin' and password == 'password'  # Change this to your preferred credentials

# Route to display the form and list of skills
@app.route('/')
def index():
    skills = get_all_skills()
    return render_template('index.html', skills=skills)

# Route to handle form submission
@app.route('/add_skill', methods=['POST'])
def add_skill():
    employee_name = request.form['employee_name']
    skill = request.form['skill']
    skill_level = request.form['skill_level']

    if employee_name and skill and skill_level:
        add_employee_skill(employee_name, skill, skill_level)
        return redirect('/')
    else:
        return "All fields are required", 400

# Admin login page
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_admin_credentials(username, password):
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid credentials", 403
    return render_template('admin_login.html')

# Admin dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    return render_template('admin_dashboard.html', skills=get_all_skills())

# Route to edit employee skill
@app.route('/edit_skill', methods=['POST'])
def edit_skill():
    old_employee_name = request.form['old_employee_name']
    old_skill = request.form['old_skill']
    old_skill_level = request.form['old_skill_level']
    
    new_employee_name = request.form['employee_name']
    new_skill = request.form['skill']
    new_skill_level = request.form['skill_level']

    edit_employee_skill([old_employee_name, old_skill, old_skill_level], [new_employee_name, new_skill, new_skill_level])
    return redirect('/admin/dashboard')

# Route to delete employee skill
@app.route('/delete_skill', methods=['POST'])
def delete_skill():
    employee_name = request.form['employee_name']
    skill = request.form['skill']
    
    delete_employee_skill(employee_name, skill)
    return redirect('/admin/dashboard')

# Logout
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

if __name__ == "__main__":
    load_or_create_csv()
    app.run(debug=True)
