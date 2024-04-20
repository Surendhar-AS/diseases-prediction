from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta

def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=1)
@app.route('/success', methods=['GET', 'POST'])
def success():
    if 'user' in session:
        if request.method == 'POST':
            entered_otp = request.form['otp']
            generated_otp = session.get('otp')
            if entered_otp == generated_otp:
                return redirect(url_for('update_password'))
            else:
                flash('OTP does not match!', 'error')
        return render_template('success.html')
    else:
        return redirect(url_for('verify'))
