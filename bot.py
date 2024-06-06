import requests
from bs4 import BeautifulSoup
import random

# AliExpress search URL for smartphones
ALIEXPRESS_URL = 'https://www.aliexpress.com/wholesale?catId=5090301&SearchText=smartphone'

# Your xman_t and xman_f cookies
COOKIES = {
    'xman_t': 'jKa2Hge0mxZzh/RT9Ut/qMUzXGYB6EKLCG3pp6d+pv0oFuBYz9VPdUhPs69vs3noJVep8XihkWgBE+qVJZDFIPRXZ/TlzOba0amxkxLAcVYPl2Dlah3P6U+Qwb4OiPY+xbThR5jKolYnddQXBPR9XEAfI5mdEJeEeJRo3n0ALhA7IAxce5RhIKXG95EbHLJsEkma8zANA8d2k77nh1bf6/bUuxmP/9dXSjqHOpFUEZJhkVMkZF0keK61p7aMKVBq/0uWzM8s4u/sJbVItL3CmMbeo6xrb9trmPpWKpGoCTDdvLkq6zJ+I9rtseUsjP8h5n2P1IxJfbB38sh5WU+h5VxxtfRz4w+QU8LnmQ8gGSWGBc+rACDVek9pBZF+GfuItLDq1h+KV+kY8ufZoXs4Gae5mNGTVNQCbZb1ZuB0Srk+Kwk6tnyWSvUhIRW3muhQCQSsn4TaRA7nZBL0CaIcro0cjMKDtHwRwj6ymLQ3ybCzdW/rA6VB9zA+QL3k1uZ2fgJ+edNAPAAAzUx+SqMVu4yYsttp0Uk6kDznepdJuhzK2gh5g3HW0cI0w4z+ul4DBs0WFKyfEYLSTLraCR0Oho3VvAPie7/2AJ8zl30EqcNK3GEzBvqga4Vz4BMdp24qPw92h6tXP9f+lHM3d8LqjtjINKcLaSD5mkTJMbFVnNBL2LJ5hwMRHBVMYU8LSYVMTR7Ziq3Tmd+yIZfFnldlvk66HRPz1D0jtMQ/SQb3CqynuMTBoH1YhDcV/U7oIO8nZBvByWFFUWrrZEMDr4RZ1TB05r+cyq99LAMeYktXdJry61NZjUsO6ALC4rGJImtE',
    'xman_f': '33iThCnKbCX6+SRTXviDprRuXT2ocNI8324fezMqW2DXdl/PHh3yo66wbpCWTYQFh0gjtWuzkdnS06Lwe/2tVDZ2Kmt1odf3MhaiXXJJfrZO8vxKrUwJZWOJZ1sMmAPZ4xNpCcSEaO5PYNiysJ7OJqlYvAyhxrFkuap7YyrlPj5moWJLv7w1gUss/qLhLlyzdjDCG9PdmB4V8eKdizKejQbkFd2uMypIL+WxPmxuAWnvgFWntjJeX4dpgDellU25j85rbaXW9inmtSSOcPJ5WdWc5Ub8oIgvvABdB5kWBcch4QA5Sybbh++IKDE4Hhnj/VvjVj38xrJYyenMrTc7EdpcxkdFdwIV6T0bBsPRk7eLm1vOSCP9pm2yfR5hu/J/gq0Zi+OhVXCN5kGezM+oZOici7HKFHJm2KAgpAMFhpkzXM2AZjtv+8nn14t44yNRmOqZs8C/CvxYveJsF5eCxU1qrCp3ed71/P4KFHPVVfaRnAoCAmNKSmI6r35B3r5p/fduleoSLAbUfEYqYLr9qW0PjzbCdhnzMlu9IbbNE9ZaIipsEGnrZbfjdrpazo2N86Ha58D90v0=',
}

# Telegram credentials
TELEGRAM_BOT_TOKEN = '7164622207:AAGHydHfvahE_xhlrRlSu8EXA1IG3vClRa0'
TELEGRAM_CHANNEL_ID = '@aliddpfree'

def fetch_products():
    response = requests.get(ALIEXPRESS_URL, cookies=COOKIES, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = []
    for item in soup.select('.JIIxO'):  # Adjust the selector based on the actual HTML structure
        title = item.select_one('.man-title-text')  # Adjust the selector based on the actual HTML structure
        link = item.select_one('a').get('href')
        image = item.select_one('img').get('src')
        price = item.select_one('.price-current').get_text()  # Adjust the selector based on the actual HTML structure

        products.append({
            'title': title,
            'link': f"https:{link}",
            'image': image,
            'price': price,
        })
    return products

def post_to_telegram(product):
    message = f"Check out this smartphone: {product['title']}\nPrice: {product['price']}\nLink: {product['link']}\nImage: {product['image']}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_CHANNEL_ID}&text={requests.utils.quote(message)}"
    response = requests.get(url)
    return response.json()

def main():
    products = fetch_products()
    if products:
        random_product = random.choice(products)
        post_to_telegram(random_product)
    else:
        print("No products found.")

if __name__ == '__main__':
    main()
