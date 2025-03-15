import requests
from bs4 import BeautifulSoup


def search_keyword(keyword):
    """Search for a keyword on Google News and return top result URL"""
    try:
        # Construct Google search URL with News tab
        query = f"https://www.google.com/search?q={keyword.replace(' ', '+')}&tbm=nws"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(query, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the first article link in News tab results
        article = soup.find('div', {'class': 'SoaBEf'})
        if article:
            article = article.find('a')

        if not article:
            print("No news articles found")
            return None
            
        # Get the article URL
        article_url = article['href']
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

def scrape_website(url):
    """Scrape a website and return its title and content"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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

if __name__ == "__main__":
    print("Starting web scraper...")
    try:
        print("Waiting for user input...")
        keyword = input("Enter a keyword to search: ").strip()
        if not keyword:
            print("Error: Please enter a valid search keyword.")
            exit(1)
            
        print(f"\nSearching Google News for: {keyword}")
        print("Making search request...")
        url = search_keyword(keyword)
        
        if url:
            print("\nScraping article...")
            print(f"Fetching URL: {url}")
            result = scrape_website(url)
            
            if result:
                print(f"\nArticle Title: {result['title']}")
                print("\nArticle Content:\n")
                print(result['content'])
            else:
                print("Error: Could not extract article content.")
        else:
            print("Error: No articles found for the given keyword.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Web scraper execution complete.")
