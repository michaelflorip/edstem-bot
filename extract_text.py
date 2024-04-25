from bs4 import BeautifulSoup
import os

def extract_text(html_path, text_path):
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Extract text and exclude script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # Rip it out

    # Get text
    text = soup.get_text()

    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    # Save the extracted text
    with open(text_path, 'w', encoding='utf-8') as file:
        file.write(text)

if __name__ == '__main__':
    html_dir = 'downloaded_pages'
    text_dir = 'extracted_text'
    os.makedirs(text_dir, exist_ok=True)

    # Loop through all downloaded HTML files
    for filename in os.listdir(html_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(html_dir, filename)
            text_file_path = os.path.join(text_dir, filename.replace('.html', '.txt'))
            extract_text(file_path, text_file_path)
            print(f'Extracted text from {filename}')
