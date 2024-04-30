from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os

base_url = "https://cdss.berkeley.edu"
target_path = "/declaring-major"
visited_urls = set()

def scrape_site(path, base_url, target_path):
    full_url = base_url + path

    # Check if URL starts with the target path and hasn't been visited
    if full_url.startswith(base_url + target_path) and full_url not in visited_urls:
        visited_urls.add(full_url)

        # Initialize WebDriver
        driver = webdriver.Chrome()

        # Navigate to the page
        driver.get(full_url)

        # Wait for the page to load fully
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))

        # Expand dropdowns or interactive elements
        dropdowns = driver.find_elements(By.CSS_SELECTOR, ".dropdown-toggle")  # Adjust selector as needed
        for dropdown in dropdowns:
            dropdown.click()

        # Extract the page source after expanding content
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Save HTML content
        save_path = os.path.join('downloaded_pages', path.strip('/').replace('/', '_') or 'index') + '.html'
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

        # Save URL in a metadata file
        metadata_path = save_path.replace('.html', '.meta.txt')
        with open(metadata_path, 'w', encoding='utf-8') as meta_file:
            meta_file.write(f"URL: {full_url}\n")

        # Find all links and recursively scrape those that match the target path
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith(target_path):
                scrape_site(href, base_url, target_path)

        driver.quit()

if __name__ == '__main__':
    # Ensure the output directory exists and is empty
    os.makedirs('downloaded_pages', exist_ok=True)
    for file in os.listdir('downloaded_pages'):
        os.remove(os.path.join('downloaded_pages', file))

    # Start scraping from the target path
    scrape_site(target_path, base_url, target_path)
