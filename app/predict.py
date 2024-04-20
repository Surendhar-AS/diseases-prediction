from flask import Flask, request, jsonify, render_template, redirect, url_for  # Import redirect and url_for
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import pandas as pd
import mysql.connector
from . import app
from flask import session
from flask import session, redirect, url_for, request
from functools import wraps
import time
from datetime import timedelta

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=1)
try:
    connection = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        passwd="Sur@1402",
        database="capstone"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM training")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = pd.DataFrame(rows, columns=columns)
except mysql.connector.Error as err:
    print("Error:", err)

features = data.drop(columns=['prognosis']).columns
scaler = StandardScaler()
scaler.fit(data.drop(columns=['prognosis']))

svm_model = SVC(kernel='linear', probability=True)
svm_model.fit(scaler.transform(data.drop(columns=['prognosis'])), data['prognosis'])

@app.route('/predict')
def index():
    if "user" in session:
        return render_template('predict.html')
    else:
        return redirect(url_for("login"))
    

@app.route('/predict', methods=['POST'])
def predict():
    # Receive symptoms from the frontend
    symptoms = request.json.get('symptoms', [])
    
    # Convert symptoms into feature vector
    symptom_indices = {symptom.strip(): i for i, symptom in enumerate(features)}
    feature_vector = [0] * len(features)
    for symptom in symptoms:
        index = symptom_indices.get(symptom.strip())
        if index is not None:
            feature_vector[index] = 1
    input_instance = pd.DataFrame([feature_vector], columns=features)
    
    # Scale the input instance
    input_instance_scaled = scaler.transform(input_instance)
    
    # Predict probabilities
    predicted_probabilities = svm_model.predict_proba(input_instance_scaled)[0]
    
    # Get top three predicted diseases and remove double quotes
    top_three_indices = predicted_probabilities.argsort()[-3:][::-1]
    top_three_diseases = [svm_model.classes_[index].strip('"') for index in top_three_indices]
    
    # Return the predicted diseases without quotes
    return jsonify({'predicted_diseases': top_three_diseases})

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
