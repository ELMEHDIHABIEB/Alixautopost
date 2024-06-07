import os
import random
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.error import TelegramError
import time

# Telegram bot token and chat ID from environment variables
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

# Initialize the bot
bot = Bot(token=telegram_bot_token)

def scrape_aliexpress_products():
    url = 'https://www.aliexpress.com/wholesale?catId=0&initiative_id=SB_20210608122644&SearchText=example'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    for item in soup.select('.JIIxO'):
        name = item.select_one('.u6k').get_text()
        price = item.select_one('.mGXnE .mGXnE').get_text()
        image = item.select_one('img')['src']
        products.append({
            'name': name,
            'price': price,
            'photo_url': image
        })

    return products

def post_random_product(products):
    try:
        random_product = random.choice(products)

        message = f"Product Name: {random_product['name']}\nPrice: {random_product['price']}"
        photo_url = random_product['photo_url']
        bot.send_photo(chat_id=telegram_chat_id, photo=photo_url, caption=message)
        print(f"Posted: {random_product['name']}")
    except TelegramError as e:
        print(f"Failed to post product: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main function to scrape and post products
def main():
    products = scrape_aliexpress_products()
    while True:
        post_random_product(products)
        time.sleep(60)  # Wait for 1 minute before posting the next product

if __name__ == "__main__":
    main()
