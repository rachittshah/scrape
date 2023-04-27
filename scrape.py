import os
import requests
from bs4 import BeautifulSoup
import urllib.request

def save_text(content, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def save_html(content, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content.prettify())

def save_images(images, folder_path):
    for idx, img in enumerate(images):
        img_url = img.get('src')
        if img_url:
            try:
                urllib.request.urlretrieve(img_url, os.path.join(folder_path, f"image_{idx}.jpg"))
            except Exception as e:
                print(f"Error downloading image {img_url}: {e}")

def scrape_url(url, folder_path):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    text = soup.get_text()
    images = soup.find_all('img')

    os.makedirs(folder_path, exist_ok=True)

    save_text(text, os.path.join(folder_path, 'text.txt'))
    save_html(soup, os.path.join(folder_path, 'html.html'))
    save_images(images, folder_path)

def main(urls, base_folder):
    for url in urls:
        folder_name = url.replace('https://', '').replace('http://', '').replace('/', '_')
        folder_path = os.path.join(base_folder, folder_name)
        print(f"Scraping {url}...")
        try:
            scrape_url(url, folder_path)
            print(f"Successfully scraped {url}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")

if __name__ == "__main__":
    urls_to_scrape = ["https://www.snowflake.com/en/", "https://asana.com/?noredirect", "https://www.mongodb.com/", "https://www.pinecone.io/", "https://www.yugabyte.com/"]
    base_folder = "scraped_data"
    main(urls_to_scrape, base_folder)
