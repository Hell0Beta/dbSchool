import datetime
from flask import Flask, flash, jsonify, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
import pyodbc
from flask import render_template

app = Flask(__name__)
app.secret_key = 'f8a9c4d6e9b7a2c3e5d8f0a1b4c6d7e8f9a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6'

# ROUTES
# :::::::::: Dashboard
@app.route('/')
def home():
    return render_template('index.html')

# :::::::::: Student Management
@app.route('/student')
def student():
    return render_template('indexed.html')



# Configuration for MS SQL Server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-9ICQ7KV/dbHealthCare?driver=ODBC+Driver+17+for+SQL+Server;Trusted_Connection=yes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Establish a connection to the database
connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-9ICQ7KV;DATABASE=dbSchool;Trusted_Connection=yes;')
cursor = connection.cursor()


if __name__ == '__main__':
    app.run(debug=True)
