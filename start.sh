#!/bin/bash
cd ~/dashboard
python3 api.py &
python3 telegram_bot.py &
sleep 5
firefox --kiosk file:///home/redj/dashboard/dashboard.html
