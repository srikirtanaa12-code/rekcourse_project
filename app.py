from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

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

def create_new_tables():
    try:
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wishlist (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                course_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_wishlist (user_id, course_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                course_id INT NOT NULL,
                rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
                review_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                platform VARCHAR(100),
                search_term VARCHAR(255),
                searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("New tables created successfully.")
    except mysql.connector.Error as err:
        print(f"Failed creating new tables: {err}")

create_database_and_table()
create_new_tables()

# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route('/')
def home():
    if 'loggedin' in session:
        return redirect(url_for('courses'))
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed.', 'error')
        return redirect(url_for('home'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    account = cursor.fetchone()
    if account:
        flash('Account already exists with that email!', 'error')
    elif not name or not email or not password:
        flash('Please fill out the form completely!', 'error')
    else:
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
    email = request.form['email']
    password = request.form['password']
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed.', 'error')
        return redirect(url_for('home'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    account = cursor.fetchone()
    if account and check_password_hash(account['password'], password):
        session['loggedin'] = True
        session['id'] = account['id']
        session['name'] = account['name']
        flash('Logged in successfully!', 'success')
        return redirect(url_for('courses'))
    else:
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

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

def get_department_from_tags(tags):
    """Determine department category from course tags"""
    tags_lower = tags.lower()
    
    if 'cyber' in tags_lower or 'security' in tags_lower:
        return 'Cyber Security'
    elif 'business' in tags_lower or 'management' in tags_lower:
        return 'Business & Management'
    elif 'finance' in tags_lower:
        return 'Finance'
    elif 'design' in tags_lower:
        return 'Design'
    elif 'science' in tags_lower:
        return 'Science'
    elif 'exam' in tags_lower:
        return 'Exam Prep'
    elif 'ml' in tags_lower or 'machine learning' in tags_lower:
        return 'Machine Learning'
    elif 'data' in tags_lower:
        return 'Data Science'
    elif 'web' in tags_lower:
        return 'Web Development'
    elif 'cloud' in tags_lower:
        return 'Cloud Computing'
    else:
        return 'Other'

@app.route('/courses')
def courses():
    if 'loggedin' not in session:
        flash('Please log in to access course recommendations.', 'error')
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    all_courses = cursor.fetchall()

    cursor.execute("SELECT course_id FROM wishlist WHERE user_id = %s", (session['id'],))
    wishlist_rows = cursor.fetchall()
    wishlist_ids = {row['course_id'] for row in wishlist_rows}

    cursor.close()
    conn.close()

    courses_by_department = {}
    
    # Department order for consistent display
    dept_order = [
        'Web Development', 'Machine Learning', 'Data Science', 'Cyber Security',
        'Business & Management', 'Finance', 'Design', 'Science', 'Exam Prep', 'Cloud Computing', 'Other'
    ]

    for course in all_courses:
        course['in_wishlist'] = course['id'] in wishlist_ids
        
        # Get department from explicit field or infer from tags
        department = course.get('department') and course['department'].strip()
        if not department:
            department = get_department_from_tags(course.get('tags', ''))
        
        if department not in courses_by_department:
            courses_by_department[department] = []
        courses_by_department[department].append(course)

    # Sort departments by defined order
    sorted_departments = {dept: courses_by_department[dept] for dept in dept_order if dept in courses_by_department}
    
    # Build safe slugs for department names (handles &, spaces, special chars)
    dept_slugs = {
        dept: re.sub(r'[^a-z0-9]+', '-', dept.lower()).strip('-')
        for dept in sorted_departments.keys()
    }

    return render_template('courses.html',
                           username=session['name'],
                           courses_by_department=sorted_departments,
                           dept_slugs=dept_slugs)


# ─────────────────────────────────────────────
# FEATURE 1 – PERSONALIZED RECOMMENDATIONS
# ─────────────────────────────────────────────

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    if 'loggedin' not in session:
        flash('Please log in to get recommendations.', 'error')
        return redirect(url_for('home'))

    recommended = []
    filters = {}

    if request.method == 'POST':
        category  = request.form.get('category', '')
        level     = request.form.get('level', '')
        cert_only = request.form.get('cert_only', '')
        filters = {'category': category, 'level': level, 'cert_only': cert_only}

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        conditions = []
        params = []
        if category:
            conditions.append("tags LIKE %s")
            params.append(f"%{category}%")
        if level:
            conditions.append("badge_type = %s")
            params.append(level.capitalize())
        if cert_only == 'on':
            conditions.append("has_cert = TRUE")

        query = "SELECT * FROM courses"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " LIMIT 20"

        cursor.execute(query, params)
        recommended = cursor.fetchall()

        if category:
            cursor.execute(
                "INSERT INTO search_logs (user_id, search_term) VALUES (%s, %s)",
                (session['id'], category)
            )
            conn.commit()

        cursor.close()
        conn.close()

    return render_template('recommendations.html',
                           username=session['name'],
                           recommended=recommended,
                           filters=filters)


# ─────────────────────────────────────────────
# FEATURE 2 – WISHLIST
# ─────────────────────────────────────────────

@app.route('/wishlist/toggle/<int:course_id>', methods=['POST'])
def toggle_wishlist(course_id):
    if 'loggedin' not in session:
        return jsonify({'error': 'not logged in'}), 401

    user_id = session['id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM wishlist WHERE user_id=%s AND course_id=%s", (user_id, course_id))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("DELETE FROM wishlist WHERE user_id=%s AND course_id=%s", (user_id, course_id))
        conn.commit()
        saved = False
    else:
        cursor.execute("INSERT INTO wishlist (user_id, course_id) VALUES (%s, %s)", (user_id, course_id))
        conn.commit()
        saved = True

    cursor.close()
    conn.close()
    return jsonify({'saved': saved})

@app.route('/wishlist')
def wishlist():
    if 'loggedin' not in session:
        flash('Please log in to view your wishlist.', 'error')
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*, w.created_at AS saved_at
        FROM courses c
        JOIN wishlist w ON c.id = w.course_id
        WHERE w.user_id = %s
        ORDER BY w.created_at DESC
    """, (session['id'],))
    saved_courses = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('wishlist.html',
                           username=session['name'],
                           saved_courses=saved_courses)


# ─────────────────────────────────────────────
# FEATURE 3 – COMPARE PLATFORMS
# ─────────────────────────────────────────────

@app.route('/compare')
def compare():
    if 'loggedin' not in session:
        flash('Please log in to compare platforms.', 'error')
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            platform,
            COUNT(*) AS total_courses,
            SUM(CASE WHEN badge_type = 'Free' THEN 1 ELSE 0 END) AS free_count,
            SUM(CASE WHEN badge_type = 'Paid' THEN 1 ELSE 0 END) AS paid_count,
            SUM(CASE WHEN has_cert = TRUE THEN 1 ELSE 0 END) AS cert_count,
            GROUP_CONCAT(DISTINCT
                CASE WHEN duration != '' THEN duration ELSE NULL END
                SEPARATOR ', '
            ) AS sample_durations
        FROM courses
        GROUP BY platform
        ORDER BY platform
    """)
    platform_stats = cursor.fetchall()

    cursor.execute("""
        SELECT c.platform, ROUND(AVG(r.rating), 1) AS avg_rating, COUNT(r.id) AS review_count
        FROM reviews r
        JOIN courses c ON r.course_id = c.id
        GROUP BY c.platform
    """)
    rating_rows = cursor.fetchall()
    ratings_map = {row['platform']: row for row in rating_rows}

    cursor.close()
    conn.close()

    for stat in platform_stats:
        p = stat['platform']
        if p in ratings_map:
            stat['avg_rating'] = ratings_map[p]['avg_rating']
            stat['review_count'] = ratings_map[p]['review_count']
        else:
            stat['avg_rating'] = 'N/A'
            stat['review_count'] = 0

    return render_template('compare.html',
                           username=session['name'],
                           platform_stats=platform_stats)


# ─────────────────────────────────────────────
# FEATURE 4 – ADMIN DASHBOARD
# ─────────────────────────────────────────────

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect('/admin')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) AS total FROM users")
    total_users = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS total FROM courses")
    total_courses = cursor.fetchone()['total']

    cursor.execute("""
        SELECT c.title, COUNT(w.id) AS save_count
        FROM wishlist w
        JOIN courses c ON w.course_id = c.id
        GROUP BY w.course_id
        ORDER BY save_count DESC
        LIMIT 1
    """)
    most_saved = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) AS total FROM reviews")
    total_reviews = cursor.fetchone()['total']

    cursor.execute("""
        SELECT search_term AS platform, COUNT(*) AS count
        FROM search_logs
        WHERE search_term != ''
        GROUP BY search_term
        ORDER BY count DESC
        LIMIT 1
    """)
    most_searched = cursor.fetchone()

    cursor.execute("""
        SELECT r.id, r.rating, r.review_text, r.created_at,
               u.name AS user_name, c.title AS course_title
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        JOIN courses c ON r.course_id = c.id
        ORDER BY r.created_at DESC
    """)
    all_reviews = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_dashboard.html',
                           courses=courses,
                           total_users=total_users,
                           total_courses=total_courses,
                           most_saved=most_saved,
                           total_reviews=total_reviews,
                           most_searched=most_searched,
                           all_reviews=all_reviews)


# ─────────────────────────────────────────────
# FEATURE 5 – REVIEWS & RATINGS
# ─────────────────────────────────────────────

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    if 'loggedin' not in session:
        flash('Please log in to view course details.', 'error')
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
    course = cursor.fetchone()
    if not course:
        cursor.close()
        conn.close()
        abort(404)

    cursor.execute("SELECT id FROM wishlist WHERE user_id=%s AND course_id=%s",
                   (session['id'], course_id))
    in_wishlist = cursor.fetchone() is not None

    cursor.execute("""
        SELECT r.*, u.name AS user_name
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.course_id = %s
        ORDER BY r.created_at DESC
    """, (course_id,))
    reviews = cursor.fetchall()

    cursor.execute("SELECT ROUND(AVG(rating),1) AS avg_rating FROM reviews WHERE course_id=%s", (course_id,))
    avg_row = cursor.fetchone()
    avg_rating = avg_row['avg_rating'] if avg_row['avg_rating'] else 0

    cursor.execute("SELECT id FROM reviews WHERE user_id=%s AND course_id=%s",
                   (session['id'], course_id))
    user_reviewed = cursor.fetchone() is not None

    cursor.close()
    conn.close()

    return render_template('course_detail.html',
                           username=session['name'],
                           course=course,
                           reviews=reviews,
                           avg_rating=avg_rating,
                           in_wishlist=in_wishlist,
                           user_reviewed=user_reviewed)

@app.route('/review/add/<int:course_id>', methods=['POST'])
def add_review(course_id):
    if 'loggedin' not in session:
        flash('Please log in to add a review.', 'error')
        return redirect(url_for('home'))

    rating      = int(request.form.get('rating', 5))
    review_text = request.form.get('review_text', '').strip()

    if rating < 1 or rating > 5:
        flash('Rating must be between 1 and 5.', 'error')
        return redirect(url_for('course_detail', course_id=course_id))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM reviews WHERE user_id=%s AND course_id=%s",
                   (session['id'], course_id))
    if cursor.fetchone():
        flash('You have already reviewed this course.', 'error')
    else:
        cursor.execute(
            "INSERT INTO reviews (user_id, course_id, rating, review_text) VALUES (%s,%s,%s,%s)",
            (session['id'], course_id, rating, review_text)
        )
        conn.commit()
        flash('Review submitted successfully!', 'success')

    cursor.close()
    conn.close()
    return redirect(url_for('course_detail', course_id=course_id))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

@app.route('/admin/review/delete/<int:review_id>')
def delete_review(review_id):
    if 'admin' not in session:
        return redirect('/admin')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reviews WHERE id = %s", (review_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Review deleted.', 'success')
    return redirect('/admin/dashboard')


# ─────────────────────────────────────────────
# ADMIN ROUTES
# ─────────────────────────────────────────────

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == os.getenv("ADMIN_PASSWORD"):
            session['admin'] = True
            return redirect('/admin/dashboard')
        else:
            return "Wrong login"
    return render_template('admin_loginn.html')

@app.route('/admin/add', methods=['POST'])
def add_course():
    if 'admin' not in session:
        return redirect('/admin')
    title       = request.form['title']
    platform    = request.form['platform']
    link        = request.form['link']
    tags        = request.form.get('tags', '')
    icon        = request.form.get('icon', '📚')
    bg_gradient = request.form.get('bg_gradient', '')
    badge_type  = request.form.get('badge_type', 'Free')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO courses (title, platform, link, tags, icon, bg_gradient, badge_type) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (title, platform, link, tags, icon, bg_gradient, badge_type)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/admin/dashboard')

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def edit_course(id):
    if 'admin' not in session:
        return redirect('/admin')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        title    = request.form['title']
        platform = request.form['platform']
        link     = request.form['link']
        tags     = request.form.get('tags', '')
        cursor.execute(
            "UPDATE courses SET title=%s, platform=%s, link=%s, tags=%s WHERE id=%s",
            (title, platform, link, tags, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/admin/dashboard')
    else:
        cursor.execute("SELECT * FROM courses WHERE id = %s", (id,))
        course = cursor.fetchone()
        cursor.close()
        conn.close()
        if not course:
            return redirect('/admin/dashboard')
        return render_template('admin_edit.html', course=course)

@app.route('/admin/delete/<int:id>')
def delete_course(id):
    if 'admin' not in session:
        return redirect('/admin')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/admin/dashboard')

if __name__ == '__main__':
    app.run(debug=True)
