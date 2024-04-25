import requests
from bs4 import BeautifulSoup
import os

base_url = "https://cdss.berkeley.edu"
start_path = "/"  # Adjust if you want to start from a specific part of the site
visited_urls = set()  # Set to store visited URLs

def scrape_site(path):
    # Normalize the path to avoid duplicate content issues
    normalized_path = os.path.normpath(path)
    full_url = base_url + normalized_path

    # Check if the URL has already been visited
    if full_url in visited_urls:
        return
    visited_urls.add(full_url)

    response = requests.get(full_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Save the current page
    save_path = os.path.join('downloaded_pages', normalized_path.strip('/').replace('/', '_') or 'index') + '.html'
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'wb') as file:
        file.write(response.content)

    # Find all links in the page and scrape them
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/') and not href.endswith('.pdf') and not href.startswith('//'):
            next_path = os.path.normpath(href)
            scrape_site(next_path)  # Recursively scrape linked pages

if __name__ == '__main__':
    scrape_site(start_path)
