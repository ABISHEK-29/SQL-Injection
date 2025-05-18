from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
import joblib
import tensorflow as tf
import xgboost as xgb
import numpy as np

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a secret key for sessions

# Load models
autoencoder = tf.keras.models.load_model('autoencoder.h5', compile=False)
autoencoder.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError())
feature_extractor = tf.keras.models.load_model('encoder_feature_extractor.h5')
vectorizer = joblib.load('tfidf_vectorizer.pkl')
xgb_model = joblib.load('xgboost_model.pkl')

# Database setup
def init_db():
    conn = sqlite3.connect('site.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            ip_address TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            username TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert an activity log
def insert_activity_log(action, username):
    conn = sqlite3.connect('site.db')
    c = conn.cursor()
    c.execute('INSERT INTO activity_logs (action, username, timestamp) VALUES (?, ?, ?)', 
              (action, username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

# Function to insert an alert
def insert_alert(input_text, ip_address):
    conn = sqlite3.connect('site.db')
    c = conn.cursor()
    c.execute('INSERT INTO alerts (input_text, timestamp, ip_address) VALUES (?, ?, ?)', 
              (input_text, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ip_address))
    conn.commit()
    conn.close()

# Function to fetch alerts
def get_alerts():
    conn = sqlite3.connect('site.db')
    c = conn.cursor()
    c.execute('SELECT input_text, timestamp, ip_address FROM alerts ORDER BY timestamp DESC')
    alerts = c.fetchall()
    conn.close()
    return alerts

# Function to fetch registered users
def get_users():
    conn = sqlite3.connect('site.db')
    c = conn.cursor()
    c.execute('SELECT username FROM users')
    users = c.fetchall()
    conn.close()
    return users

# Function to fetch activity logs
def get_activity_logs():
    conn = sqlite3.connect('site.db')
    c = conn.cursor()
    c.execute('SELECT action, username, timestamp FROM activity_logs ORDER BY timestamp DESC')
    activity_logs = c.fetchall()
    conn.close()
    return activity_logs

# Function to check for SQL injection
def is_sql_injection(input_text):
    # Vectorize
    input_vector = text_to_vector(input_text)
    # Extract Deep Features
    deep_feature = feature_extractor.predict(input_vector)
    # Predict using XGBoost
    pred = xgb_model.predict(deep_feature)
    return pred[0] == 1

# Dummy tokenizer
def text_to_vector(text):
    vector = vectorizer.transform([text]).toarray()
    return vector

# Function to register a user
def register_user(username, password):
    conn = sqlite3.connect('site.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

# Function to check if user exists
def user_exists(username):
    conn = sqlite3.connect('site.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check for SQL injection
        if is_sql_injection(username) or is_sql_injection(password):
            insert_alert(f"SQL Injection attempt during registration: {username}", request.remote_addr)
            return render_template('register.html', message="SQL Injection detected! Registration blocked.")
        
        # Check if username already exists
        if user_exists(username):
            return render_template('register.html', message="Username already exists!")
        
        # Register the user
        register_user(username, password)
        insert_activity_log('User registered', username)
        return redirect(url_for('login'))
    
    return render_template('register.html', message='')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check for SQL injection
        if is_sql_injection(username) or is_sql_injection(password):
            insert_alert(f"SQL Injection attempt during login: {username}", request.remote_addr)
            return render_template('login.html', message="SQL Injection detected! Login blocked.")
        
        # Check if username exists
        user = user_exists(username)
        if not user:
            return render_template('login.html', message="Username not found!")
        
        # Proceed with normal login
        session['username'] = username
        insert_activity_log('User logged in', username)
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', message='')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Log user viewing the dashboard
    username = session['username']
    insert_activity_log('User viewed dashboard', username)
    
    alerts = get_alerts()
    users = get_users()
    activity_logs = get_activity_logs()
    
    return render_template('dashboard.html', alerts=alerts, users=users, activity_logs=activity_logs)

@app.route('/logout')
def logout():
    username = session.get('username')
    if username:
        insert_activity_log('User logged out', username)  # Log the logout action
        session.pop('username', None)  # Clear the session
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()  # Initialize the database if not already done
    app.run(debug=True , port=8080)
