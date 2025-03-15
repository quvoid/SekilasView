from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Function to search a keyword on Google News and get the first result URL
def get_first_news_url(keyword):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up ChromeDriver
    service = Service(executable_path="/path/to/chromedriver")  # Update with your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open Google News
        driver.get("https://www.google.com")

        # Find the search box and enter the keyword
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(keyword + " news")  # Add "news" to the query
        search_box.send_keys(Keys.RETURN)

        # Wait for the page to load
        time.sleep(3)

        # Find the first news result link
        first_news_link = driver.find_element(By.CSS_SELECTOR, ".tF2Cxc a")  # Update selector if needed
        return first_news_link.get_attribute("href")
    except Exception as e:
        print(f"Error searching for keyword '{keyword}': {e}")
        return None
    finally:
        driver.quit()

# Function to scrape text content from a given URL
def scrape_website_text(url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up ChromeDriver
    service = Service(executable_path="/path/to/chromedriver")  # Update with your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the news website
        driver.get(url)

        # Wait for the page to load
        time.sleep(3)

        # Extract the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception as e:
        print(f"Error scraping website: {e}")
        return None
    finally:
        driver.quit()

# Main program
def main():
    # List of trending keywords (replace with your scraping logic)
    trending_keywords = ["Happy Holi326K", "Holi740K", "#TNBudget2025", "#CricketWorldCup"]

    print("Top Trending Keywords in India:")
    for i, keyword in enumerate(trending_keywords, 1):
        print(f"{i}. {keyword}")

    # Process each keyword
    for keyword in trending_keywords:
        print(f"\nProcessing keyword: {keyword}")

        # Step 1: Get the first news URL for the keyword
        news_url = get_first_news_url(keyword)
        if news_url:
            print(f"First news URL: {news_url}")

            # Step 2: Scrape text from the first news website
            text = scrape_website_text(news_url)
            if text:
                print(f"Text from the first news website:\n{text[:1000]}...")  # Print first 1000 characters
            else:
                print("Failed to scrape text from the website.")
        else:
            print("No news results found for this keyword.")

# Run the program
if __name__ == "__main__":
    main()