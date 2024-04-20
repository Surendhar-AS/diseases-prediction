from flask import render_template, request, redirect, url_for,session
from . import app
import mysql.connector

# MySQL database connection
connection = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    passwd="Sur@1402",
    database="capstone"
)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        password = request.form['password']
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM doctor_info WHERE doctor_id = %s AND password = %s", (doctor_id, password))
        doctor = cursor.fetchone()
        
        if doctor:
            session["user"] = doctor_id
            # Successful login, redirect to predict activity
            return redirect(url_for('predict'))
        else:
            # Failed login, show error message
            error = "Invalid credentials. Please try again."
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/forget_password')
def forget_password():
    return redirect(url_for('verify'))