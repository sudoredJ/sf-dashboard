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
    
    # Only get events within next 7 days
    seven_days = datetime.now() + timedelta(days=7)
    seven_days_str = seven_days.strftime('%Y-%m-%d')
    
    cur = db.execute('''
        SELECT id, title, date_display, event_date, time 
        FROM events 
        WHERE event_date >= date('now') 
        AND event_date <= ?
        ORDER BY event_date, time 
        LIMIT 20
    ''', (seven_days_str,))
    
    events = []
    for row in cur:
        events.append({
            'id': row[0],
            'title': row[1], 
            'date': row[2]  # This is date_display field
        })
    db.close()
    return jsonify(events)

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
