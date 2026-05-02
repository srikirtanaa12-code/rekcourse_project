from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Database configuration
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        # To handle the case where database or table might not exist
        if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            create_database_and_table()
            return mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
        return None

def create_database_and_table():
    print("Attempting to create database and table...")
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database and table created successfully.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")

# Ensure database exists on startup
create_database_and_table()

@app.route('/')
def home():
    if 'loggedin' in session:
        return redirect(url_for('courses'))
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed. Please check your settings.', 'error')
            return redirect(url_for('home'))
            
        cursor = conn.cursor()
        
        # Check if account exists
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        
        if account:
            flash('Account already exists with that email!', 'error')
        elif not name or not email or not password:
            flash('Please fill out the form completely!', 'error')
        else:
            # Insert new account
            try:
                cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', 
                               (name, email, hashed_password))
                conn.commit()
                flash('You have successfully signed up! Please log in.', 'success')
            except mysql.connector.Error as err:
                flash(f'An error occurred: {err}', 'error')
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed. Please check your settings.', 'error')
            return redirect(url_for('home'))
            
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        
        if account and check_password_hash(account['password'], password):
            # Login successful
            session['loggedin'] = True
            session['id'] = account['id']
            session['name'] = account['name']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('courses'))
        else:
            # Login failed
            flash('Incorrect email or password!', 'error')
            
        cursor.close()
        conn.close()
        
    return redirect(url_for('home'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed.', 'error')
            return redirect(url_for('home'))
            
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if account:
            return render_template('reset_password.html', email=email)
        else:
            flash('Email not found. Please sign up.', 'error')
            
    return render_template('forgot_password.html')

@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        flash('Passwords do not match!', 'error')
        return render_template('reset_password.html', email=email)
        
    hashed_password = generate_password_hash(password)
    
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed.', 'error')
        return redirect(url_for('home'))
        
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE users SET password = %s WHERE email = %s', (hashed_password, email))
        conn.commit()
        flash('Password successfully updated! You can now log in.', 'success')
    except mysql.connector.Error as err:
        flash(f'An error occurred: {err}', 'error')
        
    cursor.close()
    conn.close()
    
    return redirect(url_for('home'))

@app.route('/courses')
def courses():
    # Check if user is logged in
    if 'loggedin' in session:
        return render_template('courses.html', username=session['name'])
    
    # User is not logged in redirect to login page
    flash('Please log in to access course recommendations.', 'error')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
