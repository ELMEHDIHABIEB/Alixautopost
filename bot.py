import os
import requests
from bs4 import BeautifulSoup
import random

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_random_product():
    url = "https://www.aliexpress.com/wholesale?catId=0&initiative_id=SB_20220101000000&SearchText=smartphone"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    products = soup.find_all('a', class_='manhattan--container--1lP57Ag cards--gallery--2o6yJVt')
    random_product = random.choice(products)
    
    product_link = "https:" + random_product['href']
    product_title = random_product.find('h1', class_='manhattan--titleText--WccSjUS').text
    product_image = random_product.find('img')['src']
    
    return product_title, product_link, product_image

def send_message(product_title, product_link, product_image):
    message = f"*{product_title}*\n\nCheck it out [here]({product_link})!\n\n![Product Image]({product_image})"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=payload)
    return response.json()

def main():
    print("Sending test message...")
    product_title, product_link, product_image = get_random_product()
    response = send_message(product_title, product_link, product_image)
    print("Message sent:", response)

if __name__ == "__main__":
    main()
