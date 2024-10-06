import asyncio
from playwright.async_api import async_playwright
import time
from urllib.parse import urlparse

def clean_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

async def scrape_rails_api(base_url='https://api.rubyonrails.org/'):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        visited = set()
        to_visit = [base_url]

        while to_visit:
            url = to_visit.pop(0)
            if url in visited:
                continue

            try:
                await page.goto(url, wait_until="networkidle")
                visited.add(url)

                # Process the current page
                # (Add your scraping logic here)
                print(f"Scraped: {url}")

                # Example: Extract text content
                main_content = await page.evaluate('''
                    () => {
                        const mainElement = document.querySelector('main');
                        return mainElement ? mainElement.innerText : null;
                    }
                ''')

                if main_content:
                    print(f"Scraped main content from: {url}")
                    page_name = "_".join(url.split('/')[2:]) or 'index'
                    print(f"page_name: {page_name}")
                    #with open(f"data/{page_name}", 'w', encoding='utf-8') as f:
                    #    f.write(main_content)
                else:
                    print(f"No main content found on: {url}")

                # Find links to other pages
                links = await page.evaluate('''
                    () => Array.from(document.querySelectorAll('a[href]'))
                        .map(a => a.href)
                        .filter(href => href.startsWith(document.location.origin) || href.startsWith('/'))
                ''')

                for link in links:
                    link = clean_url(link)
                    full_url = link if link.startswith(base_url) else base_url + link.lstrip('/')
                    if full_url not in visited:
                        to_visit.append(full_url)

            except Exception as e:
                print(f"Error scraping {url}: {e}")

            # await asyncio.sleep(1)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_rails_api())
