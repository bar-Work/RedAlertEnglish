import requests
import time
import json
import os

# טעינת מילון התרגום מהקובץ
def load_translator():
    if os.path.exists('cities_en.json'):
        with open('cities_en.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

translator = load_translator()

URL = "https://www.oref.org.il/WarningMessages/alert/alerts.json"
HEADERS = {
    "Referer": "https://www.oref.org.il/",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

last_alert_id = None

print(f"🌍 English Alerts Active. Loaded {len(translator)} translations.")
print("Scanning for Real-Time Alerts...")

while True:
    try:
        response = requests.get(URL, headers=HEADERS)
        if response.status_code == 200 and response.content:
            data = response.json()
            alert_id = data.get('id')
            
            if alert_id != last_alert_id:
                last_alert_id = alert_id
                category = data.get('title', 'Alert')
                cities = data.get('data', [])
                
                # תרגום - אם לא נמצא במילון, נציג את המקור בעברית עם סימן שאלה
                en_category = translator.get(category, category)
                en_cities = [translator.get(city, f"Hebrew Only: {city}") for city in cities]
                
                print(f"\n📢 【{en_category}】")
                print(f"📍 Locations: {', '.join(en_cities)}")
                print(f"⏰ {time.strftime('%H:%M:%S')}")
                print("-" * 30)
        
    except Exception:
        pass
    time.sleep(1)
