import requests
from bs4 import BeautifulSoup
import random
import os
import time

# Replace with your bot's token and chat ID
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# URL of the AliExpress search page (modify this to target specific categories if needed)
SEARCH_URL = "https://www.aliexpress.com/wholesale?catId=0&initiative_id=SB_20210608035853&SearchText=smartphone"

def fetch_random_product():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(SEARCH_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all product containers
    product_containers = soup.find_all('a', class_='manhattan--titleText--WccSjUS')

    if not product_containers:
        return None

    # Select a random product
    product = random.choice(product_containers)
    product_title = product.get_text().strip()
    product_link = "https:" + product['href']

    # Get product image
    product_image_container = product.find_previous('img', class_='manhattan--img--low--AcYdYMN')
    product_image = product_image_container['src'] if product_image_container else None

    return {
        'title': product_title,
        'link': product_link,
        'image': product_image
    }

def send_message(product):
    message = f"**{product['title']}**\n\nCheck it out here: [Product Link]({product['link']})"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {
        'chat_id': CHAT_ID,
        'caption': message,
        'photo': product['image'],
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=payload)
    return response.json()

def main():
    while True:
        product = fetch_random_product()
        if product:
            response = send_message(product)
            print(response)
        else:
            print("No products found.")
        time.sleep(60)  # Wait for 1 minute before posting the next product

if __name__ == "__main__":
    main()
