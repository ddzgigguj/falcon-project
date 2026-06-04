# Telegram Integration Guide

## Overview

This guide explains how to integrate the Falcon Project with Telegram for notifications and bot interactions.

## Setup

### 1. Create a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the prompts to name your bot
4. Save the API token provided

### 2. Get Your Chat ID

1. Start a conversation with your bot
2. Send any message
3. Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Find the `chat.id` value in the response

### 3. Configure the Project

Add to your `.env` file:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

## Features

- **Notifications**: Receive real-time alerts via Telegram
- **Commands**: Interact with the system through bot commands
- **Reports**: Get scheduled reports delivered to your chat

## Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize the bot |
| `/status` | Get current system status |
| `/report` | Generate a quick report |
| `/help` | Show available commands |

## Sending Messages

```python
from falcon.telegram import TelegramNotifier

notifier = TelegramNotifier(token="your_token", chat_id="your_chat_id")
notifier.send_message("Hello from Falcon Project!")
```

## Troubleshooting

- **Bot not responding**: Verify the token is correct
- **Messages not delivered**: Check the chat ID
- **Rate limiting**: Telegram allows 30 messages/second per bot

## Security

- Never commit your bot token to version control
- Use environment variables or a secrets manager
- Rotate tokens if compromised via BotFather's `/revoke` command
