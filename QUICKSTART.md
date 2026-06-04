# Quick Start Guide

## Prerequisites

- Python 3.8+
- pip package manager
- Telegram account (for bot integration)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/falcon-project.git
   cd falcon-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## Basic Usage

### Starting the Application

```bash
python main.py
```

### Running Tests

```bash
python -m pytest tests/
```

### Telegram Bot Setup

1. Create a bot via [@BotFather](https://t.me/BotFather)
2. Copy the bot token
3. Add `TELEGRAM_BOT_TOKEN=your_token` to `.env`
4. Run `python test_telegram.py` to verify connection

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | Yes |
| `TELEGRAM_CHAT_ID` | Target chat ID for messages | Yes |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING) | No |

## Next Steps

- Read the full [Telegram Integration Guide](TELEGRAM_INTEGRATION.md)
- Check the [API Documentation](docs/API.md)
- Join our community on Telegram
