import csv
import requests
import datetime
import time
import random
from bs4 import BeautifulSoup
from vector import get_retriever

def get_random_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    ]
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

def scrape_nodes(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    container = soup.select_one('#page > div.c-d.c-d-e > div.bc > div.bc-cc')
    if not container:
        return []
    
    nodes = container.find_all('div', class_=lambda c: c and c.startswith('cc-cd'))
    results = []
    
    for node in nodes:
        node_id = node.get('id', '')
        if not node_id.startswith('node-'):
            continue
        
        name_elem = node.select_one('div.cc-cd-ih > div.cc-cd-is > a > div.cc-cd-lb')
        node_name = name_elem.get_text(strip=True) if name_elem else ''
        
        content_div = node.select_one('div.cc-cd-cb > div.nano-content')
        if not content_div:
            continue
            
        entries = []
        for a_tag in content_div.find_all('a', recursive=True):
            item_div = a_tag.find('div', class_='cc-cd-cb-ll')
            if not item_div:
                continue
                
            rank_span = item_div.find('span', class_='s')
            title_span = item_div.find('span', class_='t')
            extra_span = item_div.find('span', class_='e')
            
            rank = rank_span.get_text(strip=True) if rank_span else ''
            title = title_span.get_text(strip=True) if title_span else ''
            link = a_tag.get('href', '').strip()
            extra = extra_span.get_text(strip=True) if extra_span else ''
            
            entries.append({
                'node_id': node_id,
                'node_name': node_name,
                'rank': rank,
                'title': title,
                'link': link,
                'extra': extra
            })
        
        results.extend(entries)
    
    return results

if __name__ == '__main__':
    urls = [
        'https://tophub.today/c/ent?q=%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9',
        'https://tophub.today/c/ent?q=%E6%8A%96%E9%9F%B3',
        'https://tophub.today/c/ent?q=IMDB',
        'https://tophub.today/c/ent?q=AcFun',
        'https://tophub.today/c/news?q=%E7%9F%A5%E4%B9%8E'
    ]
    
    all_data = []
    
    for i, url in enumerate(urls, 1):
        headers = get_random_headers()
        print(f"[{datetime.datetime.now().isoformat()}] Fetching webpage {i}/{len(urls)}: {url}")
        print(f"Using headers: {headers['User-Agent']}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            html_content = response.text
            scrape_time = datetime.datetime.now().isoformat()
            print(f"[{datetime.datetime.now().isoformat()}] Webpage {i} fetched successfully")
        except requests.exceptions.RequestException as e:
            print(f"[{datetime.datetime.now().isoformat()}] Error fetching webpage {url}: {e}")
            continue
        
        print(f"[{datetime.datetime.now().isoformat()}] Scraping data from page {i}")
        data = scrape_nodes(html_content)
        
        for entry in data:
            entry['scrape_time'] = scrape_time
            entry['page_url'] = url
        
        all_data.extend(data)
        print(f"[{datetime.datetime.now().isoformat()}] Found {len(data)} entries on page {i}")
        
        if i < len(urls):
            wait_time = random.uniform(1, 15)
            print(f"[{datetime.datetime.now().isoformat()}] Waiting {wait_time:.2f} seconds before next scrape")
            time.sleep(wait_time)
    
    if all_data:
        print(f"[{datetime.datetime.now().isoformat()}] Writing {len(all_data)} total entries to output.csv")
        with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['node_id', 'node_name', 'rank', 'title', 'link', 'scrape_time', 'extra', 'page_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_data)
        print(f"[{datetime.datetime.now().isoformat()}] Data successfully written to output.csv")
    else:
        print(f"[{datetime.datetime.now().isoformat()}] No data found across all pages")
    
    get_retriever()