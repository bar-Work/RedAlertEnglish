cat << 'EOF' > templates/index.html
<!DOCTYPE html>
<html>
<head>
    <title>Israel Red Alert - Light Mode Live</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body, html { margin: 0; padding: 0; height: 100%; overflow: hidden; font-family: sans-serif; }
        #map { width: 100%; height: 100vh; z-index: 1; }

        /* תיבת התרעות צפה בצד שמאל למעלה */
        #floating-alerts {
            position: absolute;
            top: 20px;
            left: 20px;
            width: 300px;
            max-height: 80vh;
            overflow-y: auto;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 10px;
            pointer-events: none;
        }

        .alert-card {
            background: rgba(255, 255, 255, 0.95); /* לבן נקי עם מעט שקיפות */
            color: #333;
            padding: 15px;
            border-left: 6px solid #ff0000;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            pointer-events: auto;
            animation: slideInLeft 0.5s ease-out;
            transition: opacity 0.5s ease;
        }

        @keyframes slideInLeft {
            from { transform: translateX(-120%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        .status-indicator {
            position: absolute;
            bottom: 20px;
            right: 20px;
            padding: 5px 12px;
            background: rgba(255,255,255,0.8);
            color: #2e7d32;
            font-size: 12px;
            border-radius: 20px;
            z-index: 1000;
            font-weight: bold;
            border: 1px solid #2e7d32;
        }
    </style>
</head>
<body>
    <div id="map"></div>
    <div id="floating-alerts"></div>
    <div class="status-indicator">● LIVE CONNECTION</div>

    <script>
        var map = L.map('map', { zoomControl: false }).setView([31.5, 34.9], 8);
        L.control.zoom({ position: 'bottomright' }).addTo(map);

        // מפת Light Mode נעימה
        L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; OpenStreetMap, &copy; CARTO'
        }).addTo(map);

        var socket = io();
        var allZonesData = null; 
        var activePolygons = {}; 
        var alertStyle = { color: "#ff0000", weight: 3, fillColor: "#ff0000", fillOpacity: 0.4 };

        fetch('/zones.json').then(r => r.json()).then(data => { allZonesData = data; });

        socket.on('new_alert', function(data) {
            var container = document.getElementById('floating-alerts');
            var card = document.createElement('div');
            card.className = 'alert-card';
            
            let englishNames = data.cities.map(c => c.en).join(', ');
            card.innerHTML = `<div style="font-weight: bold; color: #d32f2f; font-size: 16px; margin-bottom: 5px;">🚨 ${data.category}</div>
                              <div style="font-size: 14px; line-height: 1.4;">${englishNames}</div>
                              <div style="font-size: 11px; color: #888; margin-top: 8px;">${data.timestamp}</div>`;
            
            container.prepend(card);

            // הסרה אוטומטית אחרי 30 שניות
            setTimeout(() => { 
                card.style.opacity = '0'; 
                setTimeout(() => card.remove(), 500); 
            }, 30000);

            if (allZonesData) {
                let bounds = L.latLngBounds(); 
                data.cities.forEach(cityObj => {
                    let heName = cityObj.he.trim();
                    let coords = allZonesData[heName];
                    if (!coords) {
                        let key = Object.keys(allZonesData).find(k => k.includes(heName));
                        if (key) coords = allZonesData[key];
                    }

                    if (coords) {
                        function fix(arr) {
                            if (arr.length === 2 && typeof arr[0] === 'number') return arr[0] > 33.5 ? [arr[1], arr[0]] : [arr[0], arr[1]];
                            return arr.map(i => fix(i));
                        }
                        if (activePolygons[heName]) map.removeLayer(activePolygons[heName]);
                        let poly = L.polygon(fix(coords), alertStyle).addTo(map);
                        poly.bindPopup(`<b>${cityObj.en}</b><br>${data.category}`);
                        activePolygons[heName] = poly;
                        bounds.extend(poly.getBounds());
                    }
                });
                if (bounds.isValid()) map.flyToBounds(bounds, { padding: [50, 50], duration: 1.5 });
            }
        });

        socket.on('remove_alert', function(data) {
            data.cities.forEach(heName => {
                if (activePolygons[heName]) {
                    map.removeLayer(activePolygons[heName]);
                    delete activePolygons[heName];
                }
            });
        });
    </script>
</body>
</html>
EOF
