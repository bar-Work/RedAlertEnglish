from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
import requests
import threading
import time
import json
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def load_translator():
    if os.path.exists('cities_en.json'):
        with open('cities_en.json', 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    return {}

translator = load_translator()

def fetch_alerts():
    url = "https://www.oref.org.il/WarningMessages/alert/alerts.json"
    headers = {
        "Referer": "https://www.oref.org.il/",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0"
    }
    
    current_active_cities = set()
    
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            api_cities = set()
            category = 'Alert'
            
            if response.status_code == 200 and len(response.content) > 2:
                data = response.json()
                api_cities = set(data.get('data', []))
                category = data.get('title', 'Alert')
            
            # 1. אזעקות חדשות שנוספו לרשימה
            added = api_cities - current_active_cities
            if added:
                en_category = translator.get(category, category)
                en_cities = [{"he": c, "en": translator.get(c, c)} for c in added]
                socketio.emit('new_alert', {"category": en_category, "cities": en_cities, "timestamp": time.strftime('%H:%M:%S')})
                
            # 2. אזעקות שהוסרו מהרשימה של פיקוד העורף
            removed = current_active_cities - api_cities
            if removed:
                socketio.emit('remove_alert', {"cities": list(removed)})
                
            current_active_cities = api_cities
        except:
            pass
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/zones.json')
def get_zones():
    return send_from_directory(os.getcwd(), 'zones.json')

if __name__ == '__main__':
    thread = threading.Thread(target=fetch_alerts)
    thread.daemon = True
    thread.start()
    socketio.run(app, debug=True, port=5001)
