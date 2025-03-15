import requests
from bs4 import BeautifulSoup

# URL of the website
url = "https://trends24.in/india/"

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the trending keywords (adjust the selector based on the website's structure)
trending_keywords = []
for item in soup.select('.trend-card__list li')[:5]:  # Adjust the selector as needed
    trending_keywords.append(item.text.strip())

# Print the top 5 trending keywords
print("Top 5 Trending Keywords in India:")
for i, keyword in enumerate(trending_keywords, 1):
    print(f"{i}. {keyword}")