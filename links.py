import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the base URL of your college website
base_url = "https://gcet.edu.in/"

# Send a request to the homepage
homepage = requests.get(base_url)
soup = BeautifulSoup(homepage.text, "html.parser")

# Extract all internal links
links = set()
for a_tag in soup.find_all("a", href=True):
    full_link = urljoin(base_url, a_tag["href"])
    if base_url in full_link:  # Ensure it's an internal link
        links.add(full_link)

# Print the extracted links
print("\n🔍 Found the following internal links:")
for link in links:
    print(link)
