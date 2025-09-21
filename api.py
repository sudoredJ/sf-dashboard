from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

@app.route('/events')
def get_events():
    db = sqlite3.connect('events.db')
    
    # Delete events that have passed
    db.execute('DELETE FROM events WHERE event_date < date("now")')
    db.commit()
    
    # Get all future events
    cur = db.execute('''
        SELECT id, title, date_display, event_date, time 
        FROM events 
        WHERE event_date >= date('now') 
        ORDER BY event_date, time
    ''')
    
    # Create a dictionary to store events by date and time
    scheduled_events = {}
    for row in cur:
        event_date = row[3]  # event_date
        time_str = row[4] if row[4] else ''  # time
        key = f"{event_date}_{time_str}"
        if key not in scheduled_events:
            scheduled_events[key] = []
        scheduled_events[key].append({
            'id': row[0],
            'title': row[1],
            'date_display': row[2]
        })
    
    # Generate time blocks starting from current time
    now = datetime.now()
    current_hour = now.hour
    
    # Round to next 3-hour block (12am, 3am, 6am, 9am, 12pm, 3pm, 6pm, 9pm)
    time_blocks = [0, 3, 6, 9, 12, 15, 18, 21]
    next_block_hour = None
    for block in time_blocks:
        if block > current_hour:
            next_block_hour = block
            break
    
    # If no block found today, start from midnight tomorrow
    if next_block_hour is None:
        start_time = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        start_time = now.replace(hour=next_block_hour, minute=0, second=0, microsecond=0)
    
    # Generate time slots (approximately 20 slots to cover ~2.5 days)
    time_slots = []
    current_slot = start_time
    
    for i in range(20):
        date_str = current_slot.strftime('%Y-%m-%d')
        hour = current_slot.hour
        
        # Format time display
        if hour == 0:
            time_display = "12am"
        elif hour < 12:
            time_display = f"{hour}am"
        elif hour == 12:
            time_display = "12pm"
        else:
            time_display = f"{hour-12}pm"
        
        # Format date display
        day_name = current_slot.strftime('%a')
        month_day = current_slot.strftime('%b %d')
        date_display = f"{day_name} {month_day} {time_display}"
        
        # Check if there are events for this date
        for key, events in scheduled_events.items():
            if key.startswith(date_str):
                for event in events:
                    time_slots.append({
                        'id': event['id'],
                        'title': event['title'],
                        'date': event['date_display']
                    })
        
        # Move to next 3-hour block
        current_slot += timedelta(hours=3)
    
    db.close()
    return jsonify(time_slots)

@app.route('/add-event', methods=['POST'])
def add_event():
    data = request.json
    db = sqlite3.connect('events.db')
    
    title = data.get('title', '')
    date_display = data.get('date', '')
    event_date = data.get('event_date', None)
    time = data.get('time', None)
    
    db.execute('INSERT INTO events (title, date_display, event_date, time) VALUES (?, ?, ?, ?)', 
               (title, date_display, event_date, time))
    db.commit()
    db.close()
    return jsonify({"status": "ok"})

app.run(host='0.0.0.0', port=5000)
