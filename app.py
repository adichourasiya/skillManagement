from flask import Flask, render_template, request, redirect, flash
import csv
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key
filename = "employee_skills.csv"

# Function to load or create CSV file
def load_or_create_csv():
    if not os.path.isfile(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Employee Name", "Skill", "Skill Level"])  # Headers
        print(f"Created new CSV file: {filename}")

# Function to add a new employee skill record
def add_employee_skill(employee_name, skill, skill_level):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([employee_name, skill, skill_level])

# Function to update an employee's skill level
def update_employee_skill(employee_name, skill, skill_level):
    skills = get_all_skills()
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Employee Name", "Skill", "Skill Level"])  # Write headers
        for existing_employee, existing_skill, existing_level in skills:
            if existing_employee == employee_name and existing_skill == skill:
                writer.writerow([employee_name, skill, skill_level])  # Update skill level
            else:
                writer.writerow([existing_employee, existing_skill, existing_level])  # Retain existing record

# Function to get all employee skills
def get_all_skills():
    if os.path.isfile(filename):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            return list(reader)
    return []

# Route to display the form and list of skills
@app.route('/')
def index():
    skills = get_all_skills()
    return render_template('index.html', skills=skills)

# Route to handle form submission for adding skills
@app.route('/add_skill', methods=['POST'])
def add_skill():
    employee_name = request.form['employee_name']
    skill = request.form['skill']
    skill_level = request.form['skill_level']

    if employee_name and skill and skill_level:
        add_employee_skill(employee_name, skill, skill_level)
        flash('Skill added successfully!', 'success')
        return redirect('/')
    else:
        flash('All fields are required.', 'error')
        return redirect('/')

# Route to handle form submission for updating skill levels
@app.route('/update_skill', methods=['POST'])
def update_skill():
    employee_name = request.form['employee_name']
    skill = request.form['skill']
    skill_level = request.form['skill_level']

    if employee_name and skill and skill_level:
        update_employee_skill(employee_name, skill, skill_level)
        flash('Skill level updated successfully!', 'success')
        return redirect('/')
    else:
        flash('All fields are required.', 'error')
        return redirect('/')

if __name__ == "__main__":
    load_or_create_csv()
    app.run(debug=True)
