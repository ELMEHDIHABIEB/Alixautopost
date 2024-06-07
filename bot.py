import requests
from bs4 import BeautifulSoup
import random
import os

# قراءة رمز البوت ومعرف المحادثة من المتغيرات البيئية
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# رابط صفحة البحث في AliExpress
SEARCH_URL = "https://www.aliexpress.com/wholesale?catId=0&initiative_id=SB_20210608035853&SearchText=smartphone"

def fetch_random_product():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, مثل Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(SEARCH_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # إيجاد جميع الحاويات المنتجات
    product_containers = soup.find_all('a', class_='manhattan--titleText--WccSjUS')

    if not product_containers:
        return None

    # اختيار منتج عشوائي
    product = random.choice(product_containers)
    product_title = product.get_text().strip()
    product_link = "https:" + product['href']

    # الحصول على صورة المنتج
    product_image_container = product.find_previous('img', class_='manhattan--img--low--AcYdYMN')
    product_image = product_image_container['src'] if product_image_container else None

    return {
        'title': product_title,
        'link': product_link,
        'image': product_image
    }

def send_message(product):
    if product:
        message = f"**{product['title']}**\n\nCheck it out here: [Product Link]({product['link']})"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        payload = {
            'chat_id': CHAT_ID,
            'caption': message,
            'photo': product['image'],
            'parse_mode': 'Markdown'
        }
    else:
        message = "I'm sorry, I can't extract products."
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }

    response = requests.post(url, data=payload)
    return response.json()

def main():
    print("Fetching random product...")
    product = fetch_random_product()
    response = send_message(product)
    print("Message sent:", response)

if __name__ == "__main__":
    main()
