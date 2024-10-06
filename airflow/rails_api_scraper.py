import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin, urlparse, urlunparse

base_url='https://api.rubyonrails.org/'

def extract_main_content(soup):
    # This function extracts the main content from the page
    # You might need to adjust this based on the actual structure of the API pages
    main_content = soup.find('main')
    if main_content:
        return main_content.get_text(strip=True)
    return "No main content found"

def scrape_rails_api():
    visited = set()
    to_visit = [base_url]
    data_dir = "data/bs4/"

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue

        print(f"Scraping: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve {url}")
            continue
        visited.add(url)

        soup = BeautifulSoup(response.text, 'html.parser')
        content = extract_main_content(soup)
        page_name = "_".join(url.split('/')[3:]) or 'index'
        with open(f"{data_dir}{page_name}.txt", 'w', encoding='utf-8') as f:
            f.write(content)

        links = extract_links(soup, url)
        for link in links:
            if link not in visited:
                to_visit.append(link)

def change_url_path(url, new_path):
    parsed_url = urlparse(url)
    new_url = parsed_url._replace(path=new_path)
    return urlunparse(new_url)

def extract_links(soup, url):
    res = []
    links = soup.find_all('a', href=True)

    for link in links:
        href = link['href']
        if not (href.startswith(base_url) or href.endswith(".html")):
            continue

        url_href = urljoin(url, href)
        parsed_url = urlparse(url_href)
        full_url = urlunparse(parsed_url._replace(fragment="", query=""))
        print(full_url, full_url.startswith(base_url))
        if full_url.startswith(base_url):
            res.append(full_url)
    return res


if __name__ == "__main__":
    scrape_rails_api()
