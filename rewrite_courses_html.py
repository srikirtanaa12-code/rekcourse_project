with open('templates/courses.html', 'r', encoding='utf-8') as f:
    content = f.read()

head_and_nav = content.split('<!-- Udemy -->')[0]
footer_and_script = '<footer class="footer">' + content.split('<footer class="footer">')[1]

jinja_template = """
    {% set platform_details = {
        'Udemy': {'logo_class': 'udemy-logo', 'logo_text': 'U', 'url': 'https://www.udemy.com'},
        'Coursera': {'logo_class': 'coursera-logo', 'logo_text': 'C', 'url': 'https://www.coursera.org'},
        'GeeksforGeeks': {'logo_class': 'gfg-logo', 'logo_text': 'G', 'url': 'https://www.geeksforgeeks.org/courses'},
        'YouTube': {'logo_class': 'youtube-logo', 'logo_text': '<i class="fab fa-youtube" style="color:white"></i>', 'url': 'https://www.youtube.com'},
        'NPTEL': {'logo_class': 'nptel-logo', 'logo_text': 'N', 'url': 'https://nptel.ac.in'},
        'Microsoft Learn': {'logo_style': 'background:#0078D4;', 'logo_text': 'M', 'url': 'https://learn.microsoft.com'}
    } %}

    {% for platform, platform_courses in courses_by_platform.items() %}
    {% set details = platform_details.get(platform, {'logo_class': '', 'logo_text': platform[0], 'url': '#'}) %}
    <section class="section" id="{{ platform|lower|replace(' ', '') }}">
        <div class="section-header">
            <div class="platform-logo {{ details.logo_class }}" {% if details.logo_style %}style="{{ details.logo_style }}"{% endif %}>{{ details.logo_text|safe }}</div>
            <h2>{{ platform }}</h2>
            <a href="{{ details.url }}" target="_blank">View All <i class="fas fa-arrow-right"></i></a>
        </div>

        <div class="cards-grid">
            {% for course in platform_courses %}
            <div class="card" data-tags="{{ course.tags }}">
                <div class="card-img" style="background: {{ course.bg_gradient if course.bg_gradient else 'none' }};">{{ course.icon }}</div>
                <div class="card-body">
                    {% if course.badge_type %}
                        {% if course.badge_type == 'Free' %}
                        <span class="card-badge badge-free">Free</span>
                        {% else %}
                        <span class="card-badge badge-paid">{{ course.badge_type }}</span>
                        {% endif %}
                    {% endif %}
                    
                    {% if course.has_cert %}
                    <span class="card-badge badge-cert">Certificate</span>
                    {% endif %}
                    
                    <h3>{{ course.title }}</h3>
                    
                    {% if course.rating or course.duration or course.views %}
                    <div class="card-meta">
                        {% if course.rating %}<span><i class="fas fa-star"></i> {{ course.rating }}</span>{% endif %}
                        {% if course.duration %}<span><i class="fas fa-clock"></i> {{ course.duration }}</span>{% endif %}
                        {% if course.views %}<span><i class="fas fa-users"></i> {{ course.views }}</span>{% endif %}
                    </div>
                    {% endif %}
                    
                    <a href="{{ course.link }}" target="_blank" class="card-link">
                        {% if course.badge_type == 'Paid' %}Enroll Now{% else %}Start Learning{% endif %}
                    </a>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>
    {% endfor %}
"""

with open('templates/courses.html', 'w', encoding='utf-8') as f:
    f.write(head_and_nav + jinja_template + footer_and_script)

print('Updated templates/courses.html')
