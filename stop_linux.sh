#!/bin/bash

echo "Stopping SF Dashboard services..."

# Kill all related processes
pkill -f "python.*api.py"
pkill -f "python.*telegram_bot.py"  
pkill -f "bore local"

echo "All services stopped."
