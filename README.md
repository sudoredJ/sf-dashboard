# SF Dashboard

Real-time event dashboard with Telegram bot integration.

## Setup

### Linux
```bash
pip3 install -r requirements.txt
cargo install bore-cli
chmod +x start_linux.sh stop_linux.sh
./start_linux.sh
```

### Windows
```bash
python api.py
python telegram_bot.py
```

## Environment

Create `.env` file:
```
BOT_TOKEN=your_telegram_bot_token_here
```

Get token from @BotFather on Telegram.

## Commands

- `/add <day> <time> <title>` - Add event
- `/list` - Show events
- `/delete <keywords>` - Delete events
- `/clear` - Clear all events