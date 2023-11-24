import requests
import sqlite3
import matplotlib.pyplot as plt

# Download 1000 posts
url = 'https://jsonplaceholder.typicode.com/posts'
response = requests.get(url)
posts = response.json()[:1000]

# Count letters in the 'body' field
letter_counts = {}
for post in posts:
    body = post['body']
    for letter in body:
        if letter.isalpha():
            letter = letter.lower()
            letter_counts[letter] = letter_counts.get(letter, 0) + 1

# Generate a frequency histogram
letters = list(letter_counts.keys())
counts = list(letter_counts.values())

plt.bar(letters, counts)
plt.xlabel('Letters')
plt.ylabel('Frequency')
plt.title('Letter Frequency in Posts Body')
plt.show()

# Connect to SQLite database (creates a new one if not exists)
conn = sqlite3.connect('example.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table to store post data if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        userId INTEGER,
        title TEXT,
        body TEXT
    )
''')

# Commit the changes
conn.commit()

# Clear the 'posts' table
cursor.execute('DELETE FROM posts')

# Commit the changes
conn.commit()

# Insert posts into the table
for post in posts:
    cursor.execute('''
        INSERT INTO posts (userId, title, body)
        VALUES (?, ?, ?)
    ''', (post['userId'], post['title'], post['body']))

# Commit the changes
conn.commit()

# Validate if the number of rows matches the expected number of posts
cursor.execute('SELECT * FROM posts')
rows = cursor.fetchall()
expected_num_posts = len(posts)
if len(rows) == expected_num_posts:
    print(f"Successfully inserted {expected_num_posts} posts into the database.")
else:
    print(f"Error: Expected {expected_num_posts} posts, but found {len(rows)} posts in the database.")

# Close the connection
conn.close()
