import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin, urlparse, urlunparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import threading
import timeit

data_dir = "data/bs4/"

def extract_main_content(soup):
    main_content = soup.find('main')
    if main_content:
        return main_content.get_text(strip=True)
    return "No main content found"

def extract_links(soup, url, base_url):
    res = []
    links = soup.find_all('a', href=True)

    for link in links:
        href = link['href']
        if not (href.startswith(base_url) or href.endswith(".html")):
            continue

        url_href = urljoin(url, href)
        parsed_url = urlparse(url_href)
        full_url = urlunparse(parsed_url._replace(fragment="", query=""))
        if full_url.startswith(base_url):
            res.append(full_url)
    return res


def scrape_page(url, base_url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve {url}")
            return None, []

        soup = BeautifulSoup(response.text, 'html.parser')
        content = extract_main_content(soup)
        new_urls = extract_links(soup, url, base_url)

        return content, new_urls
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None, []

def save_content(url, content):
    page_name = "_".join(url.split('/')[3:]) or 'index'
    print(page_name)
    #with open(f"{data_dir}{page_name}.txt", 'w', encoding='utf-8') as f:
    #    f.write(content)

def parallel_scrape_rails_api(base_url='https://api.rubyonrails.org/', max_workers=5):
    visited = set()
    to_visit = Queue()
    to_visit.put(base_url)

    lock = threading.Lock()

    def worker():
        while True:
            try:
                url = to_visit.get_nowait()
            except Queue.Empty:
                break

            with lock:
                if url in visited:
                    to_visit.task_done()
                    continue
                visited.add(url)

            print(f"Scraping: {url}")
            content, new_urls = scrape_page(url, base_url)

            if content:
                save_content(url, content)

            with lock:
                for new_url in new_urls:
                    if new_url not in visited:
                        to_visit.put(new_url)

            to_visit.task_done()
            # time.sleep(1)  # Be respectful to the server

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for _ in range(max_workers):
            futures.append(executor.submit(worker))

        # Wait for all tasks to complete
        to_visit.join()

        # Cancel any ongoing futures
        for future in futures:
            future.cancel()

# if __name__ == "__main__":
#     elapsed_time = timeit.timeit(lambda: parallel_scrape_rails_api(), number=1)
#     print("Elapse time:", elapsed_time, "seconds")
