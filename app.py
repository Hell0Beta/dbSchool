import datetime
from flask import Flask, flash, jsonify, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
import pyodbc
from flask import render_template

app = Flask(__name__)
app.secret_key = 'f8a9c4d6e9b7a2c3e5d8f0a1b4c6d7e8f9a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6'

# ROUTES
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['login-username']
        password = request.form['login-password']
        cursor.execute("SELECT * FROM Users164 WHERE username = ? AND PasswordHash = ?", (username, password))
        user = cursor.fetchone()
        if user:
            session['user'] = user[1]
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

# :::::::::: Sign Up
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        cursor.execute("SELECT * FROM Users164 WHERE username = ?", (request.form['signup-username'],))
        user = cursor.fetchone()
        if user:
            flash('Username already exists', 'danger')
            return redirect(url_for('login'))
        username = request.form['signup-username']
        password = request.form['signup-password']
        role = request.form['signup-role']
        cursor.execute("INSERT INTO Users164 (username, PasswordHash, role) VALUES (?, ?, ?)", (username, password, role))
        connection.commit()
        flash('You are successfully registered', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html')

# :::::::::: Dashboard
@app.route('/')
def home():
    context = {
        'teachers' : fetch_teachers(),
        'students' : fetch_students(),
        'totalshi' : fetch_total_shi(),
        'user' : session['user'],
        'role' : fetch_user_role()
    }
    return render_template('index.html', context = context)

# :::::::::: Student Management
@app.route('/student')
def student():
    context = {
        'teachers' : fetch_teachers(),
        'students' : fetch_students(),
        'totalshi' : fetch_total_shi(),
        'user' : session['user'],
        'role' : fetch_user_role()
    }
    return render_template('indexed.html', context=context)

# :::::::::: Teacher Management
@app.route('/teacher')
def teacher():
    context = {
        'teachers' : fetch_teachers(),
        'students' : fetch_students(),
        'totalshi' : fetch_total_shi(),
        'user' : session['user'],
        'role' : fetch_user_role()
    }
    return render_template('teachers.html', context=context)
 
# :::::::::: Course Management
@app.route('/course')
def course():
    context = {
        'course' : fetch_courses(),
        'teachers': fetch_teachers(),
        'totalshi' : fetch_total_shi(),
        'user' : session['user'],
        'role' : fetch_user_role()
    }
    return render_template('course.html', context=context)
 
#  Fetch functions
def fetch_user_role():
    user = session['user']
    print(":::::::::::: ", user)
    cursor.execute('Select role from USERS164 WHERE USERNAME = ?', user)
    
    role = cursor.fetchone()
    print("::::::::::: ",role[0])
    return role[0]

# ::::::::: Fetch all Students
def fetch_students():
    cursor.execute('Select * from Students164;')
    students = cursor.fetchall()
    return students

def fetch_teachers():
    cursor.execute('Select * from Teachers164;')
    teachers = cursor.fetchall()
    return teachers

def fetch_courses():
    cursor.execute('SELECT c.CourseID, c.CourseName, c.Credits, t.Name FROM Teachers164 t LEFT JOIN Courses164 c ON t.TeacherID = c.TeacherID;')
    courses = cursor.fetchall()
    return courses

def fetch_total_shi():
    cursor.execute('select count(Courses164.CourseID) as c, COUNT(Teachers164.TeacherID) as t, COUNT(Enrollments164.EnrollmentID) as E,COUNT(Students164.StudentID) as S from Teachers164 inner join Courses164 on Courses164.TeacherID = Teachers164.TeacherID  inner join Enrollments164 on COURSES164.CourseID  = Enrollments164.CourseID inner join Students164 on Enrollments164.StudentID = Students164.StudentID;')
    total_shi = cursor.fetchone()
    return total_shi



# Configuration for MS SQL Server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-9ICQ7KV/dbHealthCare?driver=ODBC+Driver+17+for+SQL+Server;Trusted_Connection=yes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Establish a connection to the database
connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-9ICQ7KV;DATABASE=dbSchool;Trusted_Connection=yes;')
cursor = connection.cursor()


if __name__ == '__main__':
    app.run(debug=True)
