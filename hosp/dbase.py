# generate_html.py
import mysql.connector
from jinja2 import Template

# MySQL connection
db = mysql.connector.connect(
  host="localhost",
  user="your_username",
  password="your_password",
  database="your_database"
)

# Query data ordered by points
cursor = db.cursor(dictionary=True)
cursor.execute("SELECT * FROM new_app ORDER BY points DESC")
users = cursor.fetchall()

# HTML template
template = Template('''
<html>
<head>
<!-- Your existing head content -->
</head>
<body class="bg-[var(--background-color)]">
<!-- Your existing header and search section -->

<main class="flex-1 px-4 sm:px-6 lg:px-10 py-8">
<div class="max-w-7xl mx-auto">
<!-- Your existing search and filter section -->

<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
    {% for user in users %}
    <div class="bg-[var(--background-color)] rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden flex flex-col">
        <div class="p-5 flex-grow">
            <h3 class="text-lg font-bold text-[var(--text-primary)] mb-2">{{ user.name }}</h3>
            <div class="space-y-2 text-sm text-[var(--text-secondary)]">
                <p class="flex items-center"><svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>{{ user.email }}</p>
                <p class="flex items-center"><svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>Age: {{ user.age }}</p>
                <p class="flex items-center"><svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path><path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>{{ user.address }}</p>
                <p class="flex items-center"><svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5v4m0 0h-4m4 0l-5-5" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>Weight: {{ user.weight }} lbs</p>
                <p class="flex items-center"><svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 016-6h6v6z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>Gender: {{ user.gender }}</p>
                <p class="flex items-center"><svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>Points: {{ user.points }}</p>
            </div>
        </div>
        <div class="px-5 pb-5 mt-auto">
            <button class="w-full bg-[var(--primary-color)] text-white font-bold py-2 px-4 rounded-lg hover:bg-opacity-90 transition-colors">View</button>
        </div>
    </div>
    {% endfor %}
</div>
</div>
</main>
</body>
</html>
''')

# Render template with data
html_output = template.render(users=users)

# Write to file
with open('output.html', 'w') as f:
    f.write(html_output)

db.close()