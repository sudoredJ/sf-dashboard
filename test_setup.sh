#!/bin/bash

echo "=== SF Dashboard Setup Test ==="
echo

# Check Python
echo "1. Checking Python..."
python3 --version
if [ $? -eq 0 ]; then
    echo "✓ Python3 is available"
else
    echo "✗ Python3 not found"
fi
echo

# Check pip packages
echo "2. Checking Python packages..."
python3 -c "import flask; print('✓ Flask available')" 2>/dev/null || echo "✗ Flask not installed"
python3 -c "import flask_cors; print('✓ Flask-CORS available')" 2>/dev/null || echo "✗ Flask-CORS not installed"
python3 -c "import telegram; print('✓ python-telegram-bot available')" 2>/dev/null || echo "✗ python-telegram-bot not installed"
python3 -c "import dotenv; print('✓ python-dotenv available')" 2>/dev/null || echo "✗ python-dotenv not installed"
echo

# Check Bore
echo "3. Checking Bore..."
bore --version 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ Bore is available"
else
    echo "✗ Bore not found - try: cargo install bore-cli"
fi
echo

# Check .env file
echo "4. Checking environment..."
if [ -f ".env" ]; then
    echo "✓ .env file exists"
    if grep -q "BOT_TOKEN=" .env; then
        echo "✓ BOT_TOKEN is set in .env"
    else
        echo "✗ BOT_TOKEN not found in .env"
    fi
else
    echo "✗ .env file missing - create it with: echo 'BOT_TOKEN=your_token' > .env"
fi
echo

# Test API startup
echo "5. Testing API startup..."
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from api import app
    print('✓ API imports successfully')
except Exception as e:
    print(f'✗ API import failed: {e}')
"
echo

echo "=== Setup Test Complete ==="
echo "If everything shows ✓, run: ./start_linux.sh"
