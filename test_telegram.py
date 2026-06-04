#!/usr/bin/env python3
"""
Test script for Telegram bot integration.
Verifies that the bot token and chat ID are correctly configured.
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def test_bot_connection():
    """Test if the bot token is valid."""
    print("Testing bot connection...")
    
    if not TELEGRAM_BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN is not set in .env file")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
    response = requests.get(url)
    
    if response.status_code == 200:
        bot_info = response.json()
        print(f"SUCCESS: Connected to bot @{bot_info['result']['username']}")
        return True
    else:
        print(f"ERROR: Failed to connect. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False


def test_send_message():
    """Test sending a message to the configured chat."""
    print("\nTesting message sending...")
    
    if not TELEGRAM_CHAT_ID:
        print("ERROR: TELEGRAM_CHAT_ID is not set in .env file")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": "✅ Falcon Project - Telegram integration test successful!",
        "parse_mode": "HTML"
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("SUCCESS: Test message sent successfully!")
        return True
    else:
        print(f"ERROR: Failed to send message. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False


def main():
    """Run all Telegram integration tests."""
    print("=" * 50)
    print("Falcon Project - Telegram Integration Tests")
    print("=" * 50)
    
    results = []
    results.append(test_bot_connection())
    
    if results[0]:  # Only test sending if connection works
        results.append(test_send_message())
    
    print("\n" + "=" * 50)
    if all(results):
        print("All tests PASSED! ✅")
        sys.exit(0)
    else:
        print("Some tests FAILED! ❌")
        sys.exit(1)


if __name__ == "__main__":
    main()
