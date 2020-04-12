from flask import Flask, request, jsonify, render_template, url_for, redirect, session
import os
import dialogflow
import requests
import json
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import storage
# import pusher

import pyrebase
firebaseConfig = {
    'apiKey': "AIzaSyCVuv20kGMbMNcv87Sxu0702YpLXRbdxOM",
    'authDomain': "abhayafirebase.firebaseapp.com",
    'databaseURL': "https://abhayafirebase.firebaseio.com",
    'projectId': "abhayafirebase",
    'storageBucket': "abhayafirebase.appspot.com",
    'messagingSenderId': "323947728412",
    'appId': "1:323947728412:web:18cdacc4baec42a6b719d9",
    "serviceAccount": "abhayafirebase-firebase-adminsdk-k1afh-7de12930bb.json"
   }

fa = pyrebase.initialize_app(firebaseConfig)
authe = fa.auth()

cred = credentials.Certificate('abhayafirebase-firebase-adminsdk-k1afh-7de12930bb.json')
firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route('/home')
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/donation')
def donation():
   return render_template('donation.html')

@app.route('/makedonation', methods=['POST'])
def makedonation():
   if request.method == 'POST':
      name = request.form['contact-name']
      cardno = request.form['contact-cardno']
      date = request.form['contact-date']
      cvv = request.form['contact-cvv']
      db = fa.database()
      data = {
         'name':name,
         'cardno':cardno,
         'date':date,
         'cvv':cvv
      }
      try:
         results = db.child("donation").push(data)
      except :
         return render_template('fail.html')
   return render_template('success.html')

@app.route('/signup')
def signup():
   return render_template('signup.html')

@app.route('/login')
def login():
   return render_template('login.html')

# @app.route('/dashboard')
# def dashboard():
#    if 'id' in session:
#       return render_template('dashboard.html')
#    else:
#       return render_template('login.html')

   

@app.route('/register', methods=['POST'])
def register():
   if request.method == 'POST':
      name = request.form['contact-name']
      email = request.form['contact-email']
      password = request.form['contact-pass']
      try:
         user = auth.create_user(email=email,email_verified=False, password=password,display_name=name,disabled=False)
       
      except :
         render_template('signup.html')
   return render_template('login.html')

@app.route('/makelogin', methods=['POST'])
def makelogin():
   if request.method == 'POST':
      email = request.form['contact-email']
      password = request.form['contact-pass']
      try:
         user = authe.sign_in_with_email_and_password(email,password)
         session['id'] = user['localId']  
      except :
         render_template('login.html')
   return render_template('dashboard.html')


@app.route('/logout')
def logout():
   if 'id' in session:  
        session.pop('id',None)  
   return render_template('index.html')

# def detect_intent_texts(project_id, session_id, text, language_code):
#     session_client = dialogflow.SessionsClient()
#     session = session_client.session_path(project_id, session_id)

#     if text:
#         text_input = dialogflow.types.TextInput(
#             text=text, language_code=language_code)
#         query_input = dialogflow.types.QueryInput(text=text_input)
#         response = session_client.detect_intent(
#             session=session, query_input=query_input)
#         return response.query_result.fulfillment_text

# @app.route('/abhayabot')
# def send_message():
#     message = 'hey'
#     project_id = 'abhaya-rlxqxj'
#     fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
#     response_text = { "message":  fulfillment_text }
#     print(response_text)
#     return jsonify(response_text)


if __name__ == '__main__':
   app.run()