#!/bin/bash

# SF Dashboard Linux Startup Script
cd "$(dirname "$0")"

echo "Starting SF Dashboard..."

# Kill any existing instances
pkill -f "python.*api.py" 2>/dev/null
pkill -f "python.*telegram_bot.py" 2>/dev/null
pkill -f "bore local" 2>/dev/null

# Add user bin to PATH if not already there
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

# Start API server in background
echo "Starting API server..."
python3 api.py &
API_PID=$!

# Wait a moment for API to start
sleep 3

# Test if API is responding
echo "Testing API connection..."
if curl -s http://localhost:5000/events >/dev/null 2>&1; then
    echo "✓ API is responding on port 5000"
else
    echo "✗ API not responding - check for errors above"
fi

# Start Telegram bot in background  
echo "Starting Telegram bot..."
python3 telegram_bot.py &
BOT_PID=$!

# Start Bore tunnel for API (expose port 5000)
echo "Starting Bore tunnel for API on port 5000..."
bore local 5000 --to bore.pub &
BORE_PID=$!

echo "Dashboard started!"
echo "API PID: $API_PID"
echo "Bot PID: $BOT_PID" 
echo "Bore PID: $BORE_PID"
echo ""
echo "API running on: http://localhost:5000"
echo "Bore tunnel will show public URL above"
echo ""
echo "To stop all services: ./stop_linux.sh"

# Keep script running
wait
