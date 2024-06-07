import requests
import os

# Replace with your bot's token and chat ID
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    print(response.json())  # Print response to debug
    return response.json()

def main():
    message = "Hello"
    response = send_message(message)
    print(response)  # Print response to debug

if __name__ == "__main__":
    main()
