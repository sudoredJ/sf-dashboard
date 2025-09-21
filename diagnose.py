#!/usr/bin/env python3
"""
Diagnostic script to check SF Dashboard system status
"""

import os
import sys
import sqlite3
import socket
import subprocess
import json
from pathlib import Path
from datetime import datetime
import urllib.request
import urllib.error

def check_port(port):
    """Check if a port is in use"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

def check_api():
    """Check if API is running"""
    print("[API] Status:")
    if check_port(5000):
        print("  [OK] Port 5000 is active")
        try:
            response = urllib.request.urlopen('http://localhost:5000/events', timeout=2)
            data = json.loads(response.read())
            print(f"  [OK] API responding (found {len(data)} events)")
            return True
        except Exception as e:
            print(f"  [FAIL] API not responding properly: {e}")
            return False
    else:
        print("  [FAIL] Port 5000 is not active - API not running")
        return False

def check_database():
    """Check database status"""
    print("\n[DB] Database Status:")
    db_path = Path("events.db")
    
    if not db_path.exists():
        print("  [FAIL] Database file not found (events.db)")
        return False
    
    print(f"  [OK] Database exists ({db_path.stat().st_size} bytes)")
    
    try:
        conn = sqlite3.connect('events.db')
        cur = conn.execute("SELECT COUNT(*) FROM events WHERE event_date >= date('now')")
        count = cur.fetchone()[0]
        print(f"  [OK] Database accessible ({count} upcoming events)")
        
        # Show recent events
        if count > 0:
            cur = conn.execute("""
                SELECT title, date_display, event_date 
                FROM events 
                WHERE event_date >= date('now')
                ORDER BY event_date
                LIMIT 3
            """)
            print("  Recent events:")
            for row in cur:
                print(f"    - {row[1]}: {row[0]}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"  [FAIL] Database error: {e}")
        return False

def check_processes():
    """Check running Python processes"""
    print("\n[PROC] Running Processes:")
    
    if sys.platform == "win32":
        cmd = ["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV"]
    else:
        cmd = ["ps", "aux"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout
        
        api_running = "api.py" in output
        bot_running = "telegram_bot.py" in output
        
        if api_running:
            print("  [OK] api.py is running")
        else:
            print("  [FAIL] api.py is NOT running")
            
        if bot_running:
            print("  [OK] telegram_bot.py is running")
        else:
            print("  [FAIL] telegram_bot.py is NOT running")
            
        return api_running, bot_running
    except Exception as e:
        print(f"  [WARN] Could not check processes: {e}")
        return False, False

def check_files():
    """Check if all required files exist"""
    print("\n[FILES] Required Files:")
    required_files = [
        "api.py",
        "telegram_bot.py", 
        "dashboard.html",
        "requirements.txt"
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"  [OK] {file}")
        else:
            print(f"  [FAIL] {file} - MISSING!")
            all_exist = False
    
    return all_exist

def test_add_event():
    """Test adding an event via API"""
    print("\n[TEST] Testing API Event Addition:")
    try:
        import json
        data = json.dumps({
            "title": "Test Event",
            "date_display": "Test Date",
            "event_date": datetime.now().strftime('%Y-%m-%d')
        }).encode('utf-8')
        
        req = urllib.request.Request('http://localhost:5000/add-event', 
                                    data=data,
                                    headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(req, timeout=2)
        result = json.loads(response.read())
        
        if result.get('status') == 'ok':
            print("  [OK] Successfully added test event")
            return True
        else:
            print(f"  [FAIL] Failed to add event: {result}")
            return False
    except Exception as e:
        print(f"  [FAIL] Could not test API: {e}")
        return False

def suggest_fixes(api_ok, db_ok, api_running, bot_running, files_ok):
    """Suggest fixes based on diagnostic results"""
    print("\n[ACTION] Suggested Actions:")
    
    if not files_ok:
        print("  1. Make sure all required files are in the current directory")
        return
    
    if not api_running and not bot_running:
        print("  1. Start both services:")
        print("     - python api.py")
        print("     - python telegram_bot.py")
    elif not api_running:
        print("  1. Start the API: python api.py")
    elif not bot_running:
        print("  1. Start the Telegram bot: python telegram_bot.py")
    elif not api_ok:
        print("  1. API is running but not responding. Try:")
        print("     - Stop and restart it: Ctrl+C then 'python api.py'")
    elif not db_ok:
        print("  1. Database issues detected. Try:")
        print("     - Remove database: del events.db (Windows) or rm events.db (Unix)")
        print("     - Restart services")
    else:
        print("  [OK] Everything appears to be working!")
        print("  - Open: " + os.path.join(os.getcwd(), "dashboard.html"))
        print("  - If events aren't showing, refresh the dashboard")

def main():
    print("===================================")
    print("SF Dashboard - System Diagnostic")
    print("===================================")
    
    # Run checks
    files_ok = check_files()
    api_ok = check_api()
    db_ok = check_database()
    api_running, bot_running = check_processes()
    
    # Test functionality if API is running
    if api_ok:
        test_add_event()
    
    # Provide suggestions
    suggest_fixes(api_ok, db_ok, api_running, bot_running, files_ok)
    
    print("\n===================================")

if __name__ == "__main__":
    main()
