import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def migrate():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    
    print("Dropping existing courses table if exists...")
    cursor.execute("DROP TABLE IF EXISTS courses")
    
    print("Creating new courses table...")
    cursor.execute("""
        CREATE TABLE courses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            platform VARCHAR(100) NOT NULL,
            link VARCHAR(500) NOT NULL,
            tags VARCHAR(255) DEFAULT '',
            icon VARCHAR(50) DEFAULT '📚',
            bg_gradient VARCHAR(255) DEFAULT '',
            badge_type VARCHAR(50) DEFAULT 'Free',
            has_cert BOOLEAN DEFAULT FALSE,
            rating VARCHAR(50) DEFAULT '',
            duration VARCHAR(50) DEFAULT '',
            views VARCHAR(50) DEFAULT ''
        )
    """)
    
    courses_data = [
        # Udemy
        ("Web Developer Bootcamp", "Udemy", "https://www.udemy.com/course/the-complete-web-development-bootcamp/", "web paid cert", "🌐", "linear-gradient(135deg,#1e1b4b,#4c1d95);", "Paid", True, "", "", ""),
        ("Python for Data Science and Machine Learning Bootcamp", "Udemy", "https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/", "data paid cert", "📊", "linear-gradient(135deg,#0c4a6e,#0369a1);", "Paid", True, "", "", ""),
        ("Machine Learning A-Z™", "Udemy", "https://www.udemy.com/course/machinelearning/", "ml paid cert", "🤖", "linear-gradient(135deg,#14532d,#15803d);", "Paid", True, "", "", ""),
        ("JavaScript Complete Guide", "Udemy", "https://www.udemy.com/course/javascript-the-complete-guide-2020-beginner-advanced/", "web paid", "📜", "", "Paid", False, "", "", ""),
        ("React - The Complete Guide", "Udemy", "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", "web paid", "⚛️", "", "Paid", False, "", "", ""),
        ("Angular Complete Course", "Udemy", "https://www.udemy.com/course/the-complete-guide-to-angular-2/", "web paid", "🅰️", "", "Paid", False, "", "", ""),
        ("Node.js Developer Course", "Udemy", "https://www.udemy.com/course/the-complete-nodejs-developer-course-2/", "web paid", "🟢", "", "Paid", False, "", "", ""),
        ("Docker & Kubernetes Guide", "Udemy", "https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/", "web paid", "🐳", "", "Paid", False, "", "", ""),
        ("AWS Certified Solutions Architect", "Udemy", "https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/", "cloud paid", "☁️", "", "Paid", False, "", "", ""),
        ("Complete Python Bootcamp", "Udemy", "https://www.udemy.com/course/complete-python-bootcamp/", "data paid", "🐍", "", "Paid", False, "", "", ""),

        # Coursera
        ("Machine Learning Specialization", "Coursera", "https://www.coursera.org/specializations/machine-learning-introduction", "ml paid cert", "🧠", "", "Paid", True, "", "", ""),
        ("Python for Everybody", "Coursera", "https://www.coursera.org/specializations/python", "data paid cert", "🐍", "", "Paid", True, "", "", ""),
        ("IBM Data Science Professional Certificate", "Coursera", "https://www.coursera.org/professional-certificates/ibm-data-science", "data paid cert", "📊", "", "Paid", True, "", "", ""),

        # GeeksforGeeks
        ("Python Programming Language Complete Tutorial", "GeeksforGeeks", "https://www.geeksforgeeks.org/python-programming-language/", "data free", "🐍", "linear-gradient(135deg,#052e16,#166534);", "Free", False, "", "", ""),
        ("Data Structures and Algorithms Course", "GeeksforGeeks", "https://practice.geeksforgeeks.org/courses/dsa-self-paced", "web paid cert", "📚", "linear-gradient(135deg,#1e1b4b,#4c1d95);", "Paid", True, "", "", ""),
        ("Full Stack Development Course", "GeeksforGeeks", "https://www.geeksforgeeks.org/courses/full-stack-development-with-react-node-js", "web paid cert", "💻", "linear-gradient(135deg,#1a1a2e,#16213e);", "Paid", True, "", "", ""),
        ("Machine Learning Tutorial", "GeeksforGeeks", "https://www.geeksforgeeks.org/machine-learning/", "ml free", "🤖", "linear-gradient(135deg,#2d1b69,#5b21b6);", "Free", False, "", "", ""),
        ("Java Programming Course", "GeeksforGeeks", "https://www.geeksforgeeks.org/java/", "web free", "☕", "linear-gradient(135deg,#0f172a,#1e40af);", "Free", False, "", "", ""),
        ("C++ Programming Course", "GeeksforGeeks", "https://www.geeksforgeeks.org/c-plus-plus/", "web free", "💻", "linear-gradient(135deg,#1e293b,#475569);", "Free", False, "", "", ""),
        ("DBMS Complete Course", "GeeksforGeeks", "https://www.geeksforgeeks.org/dbms/", "data free", "🗄️", "linear-gradient(135deg,#334155,#64748b);", "Free", False, "", "", ""),
        ("Operating Systems Course", "GeeksforGeeks", "https://www.geeksforgeeks.org/operating-systems/", "web free", "⚙️", "linear-gradient(135deg,#111827,#1f2937);", "Free", False, "", "", ""),
        ("Computer Networks Course", "GeeksforGeeks", "https://www.geeksforgeeks.org/computer-network-tutorials/", "web free", "🌐", "linear-gradient(135deg,#0f172a,#1e40af);", "Free", False, "", "", ""),
        ("System Design Course", "GeeksforGeeks", "https://www.geeksforgeeks.org/system-design-tutorial/", "web free", "🏗️", "linear-gradient(135deg,#065f46,#10b981);", "Free", False, "", "", ""),

        # YouTube
        ("JavaScript Full Course — Bro Code (12 hrs)", "YouTube", "https://www.youtube.com/watch?v=lfmg-EJ8gm4", "web free", "🎬", "linear-gradient(135deg,#450a0a,#991b1b);", "Free", False, "⭐ 4.9", "12 hrs", "5M+ views"),
        ("Python for Machine Learning & Data Science — freeCodeCamp", "YouTube", "https://www.youtube.com/watch?v=7eh4d6sabA0", "data ml free", "📉", "linear-gradient(135deg,#3b0764,#6d28d9);", "Free", False, "⭐ 4.9", "10 hrs", "3M+ views"),

        # NPTEL
        ("Introduction to Machine Learning — IIT Kharagpur", "NPTEL", "https://nptel.ac.in/courses/106105152", "ml free cert", "🤖", "linear-gradient(135deg,#431407,#c2410c);", "Free", True, "⭐ 4.8", "12 weeks", "100K+"),
        ("Programming in Python — IIT Bombay", "NPTEL", "https://nptel.ac.in/courses/106101183", "data free cert", "🐍", "linear-gradient(135deg,#172554,#1e3a8a);", "Free", True, "⭐ 4.7", "8 weeks", "200K+"),
        ("Data Science for Engineers", "NPTEL", "https://nptel.ac.in", "data free cert", "📊", "linear-gradient(135deg,#0f172a,#334155);", "Free", True, "⭐ 4.7", "8 weeks", "150K+"),
        ("Database Management Systems", "NPTEL", "https://nptel.ac.in", "data free cert", "🗄️", "linear-gradient(135deg,#1e293b,#475569);", "Free", True, "⭐ 4.8", "12 weeks", "300K+"),
        ("Operating Systems", "NPTEL", "https://nptel.ac.in", "web free cert", "💻", "linear-gradient(135deg,#111827,#1f2937);", "Free", True, "⭐ 4.7", "12 weeks", "250K+"),
        ("Computer Networks", "NPTEL", "https://nptel.ac.in", "web free cert", "🌐", "linear-gradient(135deg,#0f172a,#1e40af);", "Free", True, "⭐ 4.6", "10 weeks", "200K+"),
        ("Artificial Intelligence", "NPTEL", "https://nptel.ac.in", "ml free cert", "🧠", "linear-gradient(135deg,#14532d,#15803d);", "Free", True, "⭐ 4.7", "12 weeks", "180K+"),
        ("Software Engineering", "NPTEL", "https://nptel.ac.in", "web free cert", "⚙️", "linear-gradient(135deg,#4c1d95,#7c3aed);", "Free", True, "⭐ 4.6", "8 weeks", "150K+"),
        ("Cloud Computing", "NPTEL", "https://nptel.ac.in", "cloud free cert", "☁️", "linear-gradient(135deg,#1e40af,#3b82f6);", "Free", True, "⭐ 4.6", "8 weeks", "120K+"),
        ("Big Data Computing", "NPTEL", "https://nptel.ac.in", "data free cert", "📊", "linear-gradient(135deg,#065f46,#10b981);", "Free", True, "⭐ 4.7", "10 weeks", "140K+"),

        # Microsoft
        ("Azure Fundamentals (AZ-900)", "Microsoft Learn", "https://learn.microsoft.com/en-us/certifications/azure-fundamentals/", "cloud free cert", "☁️", "linear-gradient(135deg,#0f172a,#2563eb);", "Free", True, "", "", ""),
        ("Azure AI Fundamentals", "Microsoft Learn", "https://learn.microsoft.com/en-us/certifications/azure-ai-fundamentals/", "ml free cert", "🤖", "linear-gradient(135deg,#14532d,#22c55e);", "Free", True, "", "", ""),
        ("Microsoft Power BI Data Analyst", "Microsoft Learn", "https://learn.microsoft.com/en-us/certifications/power-bi-data-analyst-associate/", "data free cert", "📊", "linear-gradient(135deg,#1e3a8a,#3b82f6);", "Free", True, "", "", ""),
        ("Azure Data Fundamentals", "Microsoft Learn", "https://learn.microsoft.com/en-us/certifications/azure-data-fundamentals/", "data free cert", "📈", "linear-gradient(135deg,#0f172a,#1e40af);", "Free", True, "", "", ""),
        ("Microsoft 365 Fundamentals", "Microsoft Learn", "https://learn.microsoft.com/en-us/certifications/microsoft-365-fundamentals/", "web free cert", "💼", "linear-gradient(135deg,#4c1d95,#7c3aed);", "Free", True, "", "", ""),
        ("Azure Developer Associate", "Microsoft Learn", "https://learn.microsoft.com/en-us/certifications/azure-developer/", "web free cert", "💻", "linear-gradient(135deg,#1e1b4b,#4c1d95);", "Free", True, "", "", ""),
    ]
    
    insert_query = """
        INSERT INTO courses (title, platform, link, tags, icon, bg_gradient, badge_type, has_cert, rating, duration, views)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    print("Inserting data...")
    cursor.executemany(insert_query, courses_data)
    conn.commit()
    
    print(f"Successfully migrated {cursor.rowcount} courses.")
    cursor.close()
    conn.close()

if __name__ == '__main__':
    migrate()
