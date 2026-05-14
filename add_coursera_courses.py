import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Course data to insert - organized by sector
courses = [
    # IT
    {
        'title': 'Google IT Support Professional Certificate',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/professional-certificates/google-it-support',
        'icon': '🖥️',
        'tags': 'it support professional certificate',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    
    # Finance
    {
        'title': 'Financial Markets — Yale University',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/learn/financial-markets-global',
        'icon': '📈',
        'tags': 'finance financial markets yale',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    {
        'title': 'Introduction to Corporate Finance — Wharton',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/learn/wharton-finance',
        'icon': '💹',
        'tags': 'finance corporate finance wharton',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    {
        'title': 'Financial Accounting — University of Pennsylvania',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/learn/wharton-accounting',
        'icon': '🧾',
        'tags': 'finance accounting pennsylvania',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    {
        'title': 'Investment Management Specialization — Geneva',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/specializations/investment-management',
        'icon': '💰',
        'tags': 'finance investment management',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    {
        'title': 'FinTech: Finance Industry Transformation — HKU',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/learn/fintech',
        'icon': '💳',
        'tags': 'finance fintech transformation',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    
    # Business
    {
        'title': 'Google Project Management Professional Certificate',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/professional-certificates/google-project-management',
        'icon': '📋',
        'tags': 'business management project management',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    {
        'title': 'Business Foundations Specialization — Wharton',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/specializations/wharton-business-foundations',
        'icon': '🏢',
        'tags': 'business management wharton foundations',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    {
        'title': 'Digital Marketing Specialization — Univ. of Illinois',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/specializations/digital-marketing',
        'icon': '📣',
        'tags': 'business marketing digital',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    {
        'title': 'Leadership and Management — Macquarie University',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/learn/everyday-leadership',
        'icon': '👔',
        'tags': 'business management leadership',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    {
        'title': 'Entrepreneurship Specialization — Wharton',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/specializations/wharton-entrepreneurship',
        'icon': '🚀',
        'tags': 'business entrepreneurship wharton',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    
    # Psychology
    {
        'title': 'The Science of Well-Being — Yale University',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/learn/the-science-of-well-being',
        'icon': '🧘',
        'tags': 'psychology well-being science',
        'badge_type': 'Free',
        'has_cert': 1
    },
    {
        'title': 'Introduction to Psychology — Yale University',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/learn/introduction-psychology',
        'icon': '🧠',
        'tags': 'psychology yale introduction',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    {
        'title': 'Psychological First Aid — Johns Hopkins',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/learn/psychological-first-aid',
        'icon': '💚',
        'tags': 'psychology first aid johns hopkins',
        'badge_type': 'Free',
        'has_cert': 1
    },
    {
        'title': 'Positive Psychology Specialization — Penn',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/specializations/positivepsychology',
        'icon': '😊',
        'tags': 'psychology positive penn',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    {
        'title': 'Everyday Psychology — Duke University',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/learn/duke-psychologyone',
        'icon': '🌱',
        'tags': 'psychology duke everyday',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    
    # Design
    {
        'title': 'Google UX Design Professional Certificate',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/professional-certificates/google-ux-design',
        'icon': '🎨',
        'tags': 'design ux ui google',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    {
        'title': 'Graphic Design Specialization — CalArts',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/specializations/graphic-design',
        'icon': '🖌️',
        'tags': 'design graphic calarts',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    {
        'title': 'UI / UX Design Specialization — Michigan',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/specializations/michiganux',
        'icon': '🖥️',
        'tags': 'design ux ui michigan',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    {
        'title': 'Interaction Design Specialization — UC San Diego',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/specializations/interaction-design',
        'icon': '🖱️',
        'tags': 'design interaction ux',
        'badge_type': 'Paid',
        'has_cert': 1
    },
    {
        'title': 'Visual Elements of UI Design — CalArts',
        'platform': 'Coursera',
        'link': 'https://www.coursera.org/learn/ui-design',
        'icon': '✏️',
        'tags': 'design ui visual elements',
        'badge_type': 'Paid',
        'has_cert': 1
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
            "INSERT INTO courses (title, platform, link, icon, tags, badge_type, has_cert) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                course['title'],
                course['platform'],
                course['link'],
                course['icon'],
                course['tags'],
                course['badge_type'],
                course['has_cert']
            )
        )
    
    conn.commit()
    print(f"✅ Successfully inserted {len(courses)} Coursera courses!")
    print("\nCourses added by sector:")
    print("  • IT: 1 course")
    print("  • Finance: 5 courses")
    print("  • Business & Management: 5 courses")
    print("  • Psychology: 5 courses")
    print("  • Design: 5 courses")
    
    cursor.close()
    conn.close()
    
except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
