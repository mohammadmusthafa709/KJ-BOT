import requests
from bs4 import BeautifulSoup
import re
import time

# Base website URL
BASE_URL = "https://www.kristujayanti.edu.in/"
visited_links = set()  # To avoid visiting the same page multiple times

# Function to scrape a single page
def scrape_page(url):
    """Scrapes text content from a given URL."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text_elements = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li"])
            
            extracted_text = []
            for element in text_elements:
                cleaned_text = re.sub(r'\s+', ' ', element.get_text(strip=True))
                extracted_text.append(cleaned_text)
            
            return "\n".join(extracted_text)
        else:
            print(f"❌ Failed to fetch {url} | Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Error scraping {url}: {e}")
        return None

# Function to get all internal links from a page
def get_internal_links(url):
    """Finds all internal links on a webpage."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            links = []
            
            for a_tag in soup.find_all("a", href=True):
                link = a_tag["href"]
                
                # Ensure link is within the same website
                if link.startswith("/") or BASE_URL in link:
                    full_link = link if BASE_URL in link else BASE_URL + link.lstrip("/")
                    
                    if full_link not in visited_links:
                        links.append(full_link)
                        visited_links.add(full_link)
            
            return links
        else:
            return []
    except Exception as e:
        print(f"⚠️ Error fetching links from {url}: {e}")
        return []

# Main function to scrape the website
def scrape_website(start_url):
    """Scrapes all internal pages of the website."""
    pages_to_scrape = [start_url]
    all_data = []

    while pages_to_scrape:
        current_url = pages_to_scrape.pop(0)
        if current_url in visited_links:
            continue

        print(f"🔍 Scraping: {current_url}")
        visited_links.add(current_url)

        # Scrape current page
        page_text = scrape_page(current_url)
        if page_text:
            all_data.append(f"URL: {current_url}\n{page_text}\n" + "-"*80)

        # Find new links
        new_links = get_internal_links(current_url)
        pages_to_scrape.extend(new_links)

        time.sleep(1)  # Be nice to the server :)

    # Save all extracted data
    with open("college_full_data.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(all_data))

    print("✅ Full website scraping complete! Data saved to college_full_data.txt")

# Start the scraping process
scrape_website(BASE_URL)
