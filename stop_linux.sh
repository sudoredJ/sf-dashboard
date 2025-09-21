#!/bin/bash

echo "Stopping SF Dashboard services..."

# Kill all related processes (only user's processes)
pkill -f "python.*api.py" 2>/dev/null
pkill -f "python.*telegram_bot.py" 2>/dev/null
pkill -f "bore local" 2>/dev/null

echo "All services stopped."
