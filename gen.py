import random
import string
import requests
import time

# Configuration
WEBHOOK_URL = 'Webhook URL'# Replace with your Discord webhook URL
VALID_CODES_FILE = 'valid_codes.txt'

def generate_random_string(length=18):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def send_to_discord(webhook_url, message):
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print(f"Failed to send message to Discord. Status code: {response.status_code}, Response: {response.text}")

def check_code(code):
    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    response = requests.get(url)
    return response.status_code

def save_valid_code(code):
    with open(VALID_CODES_FILE, 'a') as file:
        file.write(f"{code}\n")

def main():
    while True:
        code = generate_random_string()
        
        status_code = check_code(code)
        
        if status_code == 200:
            print(f"Valid code found: {code}")
            send_to_discord(WEBHOOK_URL, f"Valid code found: discord.gift/{code}")
            save_valid_code(code)
        else:
            print(f"Invalid code: {code}")
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()
