import requests

# Downloading posts from site
url = 'https://jsonplaceholder.typicode.com/posts'
response = requests.get(url)
posts = response.json()

# Dict init for letter count
letter_count = {}
for letter in 'abcdefghijklmnopqrstuvwxyz':
    letter_count[letter] = 0

# Processing every post
for post in posts:
    if 'body' in post:
        body = post['body'].lower()  # Changing letters to lower for cohesion
        for char in body:
            if char.isalpha():
                letter_count[char] += 1

# Printing the output in console
for letter, count in letter_count.items():
    print(f"{letter}: {count}")

# Graphical oputput
import matplotlib.pyplot as plt

letters = letter_count.keys()
counts = letter_count.values()

plt.bar(letters, counts)
plt.xlabel('Letter')
plt.ylabel('Number of occurrences')
plt.title('The number of occurrences of letters in the body of post')
plt.show()
