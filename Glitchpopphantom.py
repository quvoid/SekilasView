import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# Function to get the top trending keyword from Trends24.in
def get_trending_keyword():
    url = "https://trends24.in/india/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first trending keyword
    trending_keyword = soup.select_one('.trend-card__list li')  # Adjust the selector as needed
    if trending_keyword:
        return trending_keyword.text.strip()
    else:
        return None

# Function to search for a keyword on Google, navigate to the News tab, and return the first result URL
def search_keyword(keyword):
    try:
        # Construct Google search URL
        query = f"https://www.google.com/search?q={quote(keyword)}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }

        response = requests.get(query, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Debugging: Print the HTML content of the Google search page
        # print(soup.prettify())

        # Find the "News" tab link
        news_tab_link = soup.find('a', {'href': True, 'data-hveid': True, 'data-ved': True, 'aria-label': 'News'})
        if not news_tab_link:
            print("News tab not found on Google search results.")
            return None

        # Construct the full URL for the News tab
        news_tab_url = "https://www.google.com" + news_tab_link['href']
        print(f"Navigating to News tab: {news_tab_url}")

        # Send a request to the News tab URL
        response = requests.get(news_tab_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the first news result link
        first_news_link = soup.find('div', {'class': 'tF2Cxc'})  # Updated selector
        if first_news_link:
            first_news_link = first_news_link.find('a')

        if not first_news_link:
            print("No news articles found in the News tab.")
            return None
            
        # Get the article URL
        article_url = first_news_link['href']
        if article_url.startswith('/url?'):
            # Parse Google's redirect URL
            from urllib.parse import parse_qs, urlparse
            parsed = urlparse(article_url)
            qs = parse_qs(parsed.query)
            article_url = qs.get('q', [article_url])[0]
            
        print(f"Found article URL: {article_url}")
        return article_url
    except requests.exceptions.RequestException as e:
        print(f"Error searching for keyword: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Function to scrape a website and return its title and content
def scrape_website(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=20)  # 20 second timeout
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else 'No Title'
        # Get all text content, stripping extra whitespace
        text_content = ' '.join(soup.stripped_strings)
        
        return {
            'title': title,
            'content': text_content
        }
    except requests.exceptions.Timeout:
        print(f"Timeout error: The request to {url} took too long")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error scraping website {url}: {e}")
        return None

# Main program
def main():
    print("Starting web scraper...")
    try:
        # Step 1: Get the top trending keyword from Trends24.in
        print("Fetching the top trending keyword from Trends24.in...")
        trending_keyword = get_trending_keyword()

        if not trending_keyword:
            print("Error: No trending keyword found.")
            return

        print(f"\nTop Trending Keyword in India: {trending_keyword}")

        # Step 2: Search for the keyword on Google and navigate to the News tab
        print("Searching Google for the keyword and navigating to the News tab...")
        article_url = search_keyword(trending_keyword)

        if not article_url:
            print("Error: No news articles found for the keyword.")
            return

        # Step 3: Scrape the first news article
        print("\nScraping the first news article...")
        result = scrape_website(article_url)

        if result:
            print(f"\nArticle Title: {result['title']}")
            print("\nArticle Content:\n")
            print(result['content'])
        else:
            print("Error: Could not extract article content.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("\nWeb scraper execution complete.")

# Run the program
if __name__ == "__main__":
    main()