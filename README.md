# SF Dashboard

A real-time event dashboard with Telegram bot integration and web interface.

## Features

- 🌐 **Web Dashboard** - Real-time updating HTML interface
- 🤖 **Telegram Bot** - Add/remove events via Telegram commands  
- ⏰ **Time Blocks** - Shows upcoming 3-hour time slots
- 🔄 **Auto-Update** - Dashboard refreshes every 3 seconds
- 🌍 **Public Access** - Expose via Bore tunnels

## Quick Start

### Windows
```bash
python api.py
# In another terminal:
python telegram_bot.py
# Open dashboard.html in browser
```

### Linux (Recommended)
```bash
# Install dependencies
pip3 install -r requirements.txt

# Install Bore tunnel tool
cargo install bore-cli
# OR download from: https://github.com/ekzhang/bore/releases

# Setup environment
cp .env.example .env
# Edit .env with your bot token

# Make scripts executable
chmod +x start_linux.sh stop_linux.sh

# Start everything
./start_linux.sh
```

## Environment Setup

1. **Get Telegram Bot Token:**
   - Message @BotFather on Telegram
   - Send `/newbot` and follow instructions
   - Copy the token

2. **Create .env file:**
   ```
   BOT_TOKEN=your_telegram_bot_token_here
   ```

## Telegram Bot Commands

- `/add <day> <time> <title>` - Add event
  - Examples: `/add tomorrow 2pm Meeting`, `/add tue 9am Doctor`
- `/list` - Show upcoming events  
- `/delete <keywords>` - Delete events matching keywords
- `/clear` - Clear all events

## API Endpoints

- `GET /events` - Get time blocks with events
- `POST /add-event` - Add new event

## Bore Tunnel Usage

The `start_linux.sh` script automatically starts a Bore tunnel exposing your API publicly:

```bash
bore local 5000 --to bore.pub
```

This gives you a public URL like `https://abc123.bore.pub` that anyone can access.

## File Structure

```
sf-dashboard/
├── api.py              # Flask API server
├── telegram_bot.py     # Telegram bot
├── dashboard.html      # Web interface
├── events.db          # SQLite database (auto-created)
├── requirements.txt   # Python dependencies
├── start_linux.sh     # Linux startup script
├── stop_linux.sh      # Stop all services
└── .env              # Environment variables (create this)
```

## Deployment Notes

- Dashboard shows 20 time blocks (~2.5 days) starting from current time
- Time blocks are 3-hour intervals: 12am, 3am, 6am, 9am, 12pm, 3pm, 6pm, 9pm
- Events automatically populate in appropriate time slots
- Free time slots show "─── Free Time ───"
- Database is shared between web interface and Telegram bot

## Troubleshooting

**Telegram bot not working?**
- Check your .env file has the correct BOT_TOKEN
- Verify token with @BotFather using `/mybots`

**API not accessible?**
- Check if port 5000 is available: `netstat -tlnp | grep :5000`
- Try a different port in api.py if needed

**Bore tunnel issues?**
- Install latest version: `cargo install bore-cli`  
- Try different server: `bore local 5000 --to your-server.com`