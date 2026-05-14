import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Course data to insert
courses = [
    {
        'title': 'Web Development Full Course — Thetips4you',
        'platform': 'YouTube',
        'link': 'https://www.youtube.com/watch?v=6Xj-o-HiUFQ',
        'duration': '10 Hours',
        'icon': '🌐',
        'tags': 'web development free'
    },
    {
        'title': 'Full Stack Web Development — WsCube Tech',
        'platform': 'YouTube',
        'link': 'https://www.youtube.com/watch?v=HVjjoMvutj4',
        'duration': '28 Hours',
        'icon': '💻',
        'tags': 'full stack web development free'
    },
    {
        'title': 'Frontend Development Complete Course — Great Learning',
        'platform': 'YouTube',
        'link': 'https://www.youtube.com/watch?v=zJSY8tbf_ys',
        'duration': '43+ Hours',
        'icon': '🎨',
        'tags': 'frontend development free'
    },
    {
        'title': 'Web Development Full Course — Bro Code',
        'platform': 'YouTube',
        'link': 'https://www.youtube.com/watch?v=HD13eq_Pmp8',
        'duration': '28+ Hours',
        'icon': '🚀',
        'tags': 'web development free'
    },
    {
        'title': 'React JS Full Course — freeCodeCamp',
        'platform': 'YouTube',
        'link': 'https://www.youtube.com/watch?v=bMknfKXIFA8',
        'duration': '12 Hours',
        'icon': '⚛️',
        'tags': 'react web development free'
    },
    {
        'title': 'MERN Stack Full Course — Simplilearn',
        'platform': 'YouTube',
        'link': 'https://www.youtube.com/watch?v=7CqJlxBYj-M',
        'duration': '11 Hours',
        'icon': '🔥',
        'tags': 'mern stack web development free'
    },
    {
        'title': 'HTML & CSS Complete Course — SuperSimpleDev',
        'platform': 'YouTube',
        'link': 'https://www.youtube.com/watch?v=G3e-cpL7ofc',
        'duration': '6 Hours',
        'icon': '📚',
        'tags': 'html css web development free'
    },
    {
        'title': 'JavaScript Full Course — Bro Code',
        'platform': 'YouTube',
        'link': 'https://www.youtube.com/watch?v=lfmg-EJ8gm4',
        'duration': '12 Hours',
        'icon': '🟨',
        'tags': 'javascript web development free'
    }
]

try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    
    for course in courses:
        cursor.execute(
            "INSERT INTO courses (title, platform, link, duration, icon, tags, badge_type) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                course['title'],
                course['platform'],
                course['link'],
                course['duration'],
                course['icon'],
                course['tags'],
                'Free'
            )
        )
    
    conn.commit()
    print(f"✅ Successfully inserted {len(courses)} YouTube courses!")
    
    cursor.close()
    conn.close()
    
except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
