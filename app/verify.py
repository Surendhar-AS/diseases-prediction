# verify.py
from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import random
import string
from flask_mail import Mail, Message


connection = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    passwd="Sur@1402",
    database="capstone"
)

app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]='surendharas1402@gmail.com'
app.config['MAIL_PASSWORD']='oazt xxxc vnyp rgni'                    #you have to give your password of gmail account
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)

# Generate OTP
def generate_otp():
    numbers = ''.join(random.choices(string.digits, k=3))
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    return numbers + letters
otp = generate_otp()
# Send Email OTP
def send_email_otp(email, otp):
    msg = Message('OTP for Password Reset', sender='surendharas1402@gmail.com', recipients=[email])
    msg.body = f'Your OTP for Reset/Forgot password is: {otp}.\n\nThis is an auto generated mail. Kindly don\'t reply or send message to this mail id.'
    mail.send(msg)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        email = request.form['email']
        phone = request.form['phone']
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM doctor_info WHERE doctor_id = %s", (doctor_id,))
        doctor = cursor.fetchone()
        
        if doctor:
            if doctor['email'] == email and doctor['phone'] == phone:
                otp = generate_otp()
                session["user"] = doctor_id
                session["otp"] = otp  # Store OTP in session
                session["email"] = email  # Store email in session
                session["phone"] = phone# Store OTP in session
                send_email_otp(email, otp)
                flash('OTP has been sent to your registered email', 'success')
                return redirect(url_for('success'))
            else:
                flash('Email and phone number do not match the doctor ID.', 'error')
        else:
            flash('Invalid doctor ID.', 'error')
    
    return render_template('index.html')