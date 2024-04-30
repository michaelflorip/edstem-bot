from graphviz import Digraph
import os
from urllib.parse import urljoin, urlparse

def build_visual_site_map(urls_file, base_url):
    dot = Digraph(comment='Data Science Major Site Map')

    # Read the URLs from the file
    with open(urls_file, 'r') as f:
        urls = [url.strip() for url in f.readlines() if url.strip()]

    # Create a dictionary to map URLs to their simplified node names
    url_to_name = {}

    # Create nodes for each unique URL
    for url in urls:
        if url.startswith(base_url):
            # Create a simplified name for the URL
            parsed_url = urlparse(url)
            if parsed_url.path:
                short_name = parsed_url.path.strip('/').replace('/', '_')
                short_name = short_name if short_name else 'root'
                url_to_name[url] = short_name
                dot.node(short_name, short_name)

    # Create edges based on URL hierarchy
    for url in urls:
        if url.startswith(base_url):
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.strip('/').split('/')
            for i in range(1, len(path_parts)):
                # Construct the parent and child URL
                parent_path = '/'.join(path_parts[:i])
                child_path = '/'.join(path_parts[:i+1])
                parent_url = urljoin(base_url, parent_path)
                child_url = urljoin(base_url, child_path)
                parent_name = url_to_name.get(parent_url, 'root')
                child_name = url_to_name.get(child_url, '')
                if parent_name and child_name:
                    dot.edge(parent_name, child_name)

    # Render and view the visual site map
    dot.render('data_science_major_site_map', view=True)

if __name__ == '__main__':
    base_url = "https://cdss.berkeley.edu/academics/data-science-undergraduate-studies/data-science-major"
    urls_file = 'data_science_major_urls.txt'
    build_visual_site_map(urls_file, base_url)
