from bs4 import BeautifulSoup
import os

def extract_text(html_path, text_path):
    # Read the associated URL from the .meta.txt file
    meta_path = html_path.replace('.html', '.meta.txt')
    if os.path.exists(meta_path):
        with open(meta_path, 'r', encoding='utf-8') as meta_file:
            url_info = meta_file.read().strip()
    else:
        url_info = "URL: Not Available"

    # Parse the HTML content
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Remove scripts and style elements
    for script in soup(["script", "style"]):
        script.extract()

    # Extract text content
    text = soup.get_text()

    # Clean and organize text content
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    # Save the URL and text content
    with open(text_path, 'w', encoding='utf-8') as file:
        file.write(f"{url_info}\n\n{text}")

if __name__ == '__main__':
    html_dir = 'downloaded_pages'
    text_dir = 'extracted_text'
    os.makedirs(text_dir, exist_ok=True)

    # Process all HTML files
    for filename in os.listdir(html_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(html_dir, filename)
            text_file_path = os.path.join(text_dir, filename.replace('.html', '.txt'))
            extract_text(file_path, text_file_path)
            print(f'Extracted text from {filename} to {text_file_path}')
