from flask import Flask, request, jsonify, render_template
from datetime import datetime
import json

app = Flask(__name__)

def load_students():
    with open('students.json') as f:
        return json.load(f)

@app.route('/')
def home():
    return open('index.html').read()

@app.route('/find-student', methods=['POST'])
def find_student():
    standard = request.form['standard']
    section = request.form['section']
    roll = request.form['roll']
    
    students = load_students()
    for student in students:
        if student['standard'] == standard and student['section'] == section and student['roll'] == roll:
            return jsonify({'found': True, 'name': student['name']})
    
    return jsonify({'found': False})

@app.route('/check', methods=['POST'])
def check():
    standard = request.form['standard']
    section = request.form['section']
    roll = request.form['roll']
    dob_input = request.form['dob']  # Received as YYYY-MM-DD from <input type="date">

    # Convert to match JSON format: YYYY/MM/DD
    try:
        dob_formatted = datetime.strptime(dob_input, '%Y-%m-%d').strftime('%Y/%m/%d')
    except ValueError:
        return "Invalid date format. Please select a valid date."

    students = load_students()
    for student in students:
        if (student['standard'] == standard and 
            student['section'] == section and 
            student['roll'] == roll and 
            student['dob'] == dob_formatted):
            return render_template('marksheet.html', student=student)
    
    return "Access denied due to Invalid DOB.Kindly contact RSS school Administrator to check DOB as per the records."

if __name__ == '__main__':
    app.run(debug=True)