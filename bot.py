import requests
from bs4 import BeautifulSoup
from telegram import Bot
import os 

# Get the bot token and channel ID from environment variables
BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']  # Replace with your channel ID

bot = Bot(token=BOT_TOKEN)

def scrape_aliexpress():
    url = 'https://www.aliexpress.com/wholesale?catId=0&initiative_id=SB_20210608052432&SearchText=your+search+term'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = []

    for item in soup.select('.item'):  # Adjust the selector to match the AliExpress HTML structure
        title = item.select_one('.item-title').get_text(strip=True)
        price = item.select_one('.price').get_text(strip=True)
        image_url = item.select_one('.item-img img')['src']
        
        products.append({
            'title': title,
            'price': price,
            'image_url': image_url
        })

    return products

def post_to_channel():
    products = scrape_aliexpress()
    
    for product in products:
        message = f"Title: {product['title']}\nPrice: {product['price']}\n"
        bot.send_photo(chat_id=CHANNEL_ID, photo=product['image_url'], caption=message)

if __name__ == "__main__":
    post_to_channel()
