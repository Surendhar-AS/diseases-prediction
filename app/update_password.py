# verify.py
from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from datetime import timedelta

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=1)
connection = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    passwd="Sur@1402",
    database="capstone"
)

@app.route('/update_password', methods=['GET', 'POST'])
def update_password():
    if 'user' in session:  # Check if user is logged in
        if request.method == 'POST':
            doctor_id = session.get('user')
            new_password = request.form['new_password']
            retype_password = request.form['retype_password']

            # Password validation
            if len(new_password) < 8 or len(new_password) > 12:
                flash("Password length must be between 8 to 12 characters.", "error")
                return redirect(url_for('update_password'))
            if not any(char.isupper() for char in new_password):
                flash("Password must contain at least one uppercase letter.", "error")
                return redirect(url_for('update_password'))
            if not any(char.islower() for char in new_password):
                flash("Password must contain at least one lowercase letter.", "error")
                return redirect(url_for('update_password'))
            if not any(char.isdigit() for char in new_password):
                flash("Password must contain at least one digit.", "error")
                return redirect(url_for('update_password'))
            if not any(not char.isalnum() for char in new_password):
                flash("Password must contain at least one special character.", "error")
                return redirect(url_for('update_password'))
            if new_password != retype_password:
                flash("Passwords do not match.", "error")
                return redirect(url_for('update_password'))

            # Update password in the database
            cursor = connection.cursor()
            cursor.execute("UPDATE doctor_info SET password = %s WHERE doctor_id = %s", (new_password, doctor_id))
            connection.commit()
            flash("Password updated successfully.", "success")
            return redirect(url_for('update_password'))
        else:
            return render_template('update_password.html')
    else:
        return redirect(url_for('verify'))  # Redirect to login if user is not logged in

@app.route('/go_to_login')
def go_to_login():
    session.pop("user", None)
    return redirect(url_for('login'))
