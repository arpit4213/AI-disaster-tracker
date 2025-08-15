from fastapi import FastAPI
from datetime import datetime
import pytz
import requests
from fastapi.staticfiles import StaticFiles

a = FastAPI()
a.mount("/static", StaticFiles(directory="static"), name="static")

CITIES = [
    {"name": "Delhi", "lat": 28.6139, "lon": 77.2090},
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639},
    {"name": "Chennai", "lat": 13.0827, "lon": 80.2707},
    {"name": "Bengaluru", "lat": 12.9716, "lon": 77.5946},
    {"name": "Hyderabad", "lat": 17.3850, "lon": 78.4867},
    {"name": "Ahmedabad", "lat": 23.0225, "lon": 72.5714},
    {"name": "Pune", "lat": 18.5204, "lon": 73.8567},
    {"name": "Jaipur", "lat": 26.9124, "lon": 75.7873},
    {"name": "Lucknow", "lat": 26.8467, "lon": 80.9462},
    {"name": "Kochi", "lat": 9.9312, "lon": 76.2673},
    {"name": "Guwahati", "lat": 26.1445, "lon": 91.7362},
    {"name": "Bhopal", "lat": 23.2599, "lon": 77.4126},
    {"name": "Patna", "lat": 25.5941, "lon": 85.1376},
    {"name": "Bhubaneswar", "lat": 20.2961, "lon": 85.8245},
]

@a.get("/")
def read_root():
    return {"message": "DisasterGuard API is running!"}

def sev_from_mm(mm: float) -> str:
    if mm >= 15: return "High"
    if mm >= 5: return "Medium"
    return "Low"

@a.get("/alerts")
def get_alerts():
    ist = pytz.timezone("Asia/Kolkata")
    now_ist = datetime.now(ist).isoformat()
    alerts = []

    try:
        for c in CITIES:
            url = (
                "https://api.open-meteo.com/v1/forecast"
                f"?latitude={c['lat']}&longitude={c['lon']}"
                "&hourly=precipitation,weathercode&forecast_days=1&timezone=Asia%2FKolkata"
            )
            r = requests.get(url, timeout=6)
            j = r.json()
            times = j.get("hourly", {}).get("time", [])
            rain = j.get("hourly", {}).get("precipitation", [])
            codes = j.get("hourly", {}).get("weathercode", [])
            if not times or not rain: 
                continue
            max_mm = 0.0
            max_t = times[0]
            for i in range(min(len(times), len(rain))):
                mm = rain[i] or 0.0
                code = codes[i] if i < len(codes) else None
                if code in [95, 96, 99]:
                    mm = max(mm, 10.0)
                if mm > max_mm:
                    max_mm = mm
                    max_t = times[i]
            if max_mm >= 1.0:
                alerts.append({
                    "id": f"rain_{c['name']}",
                    "type": "Rain Alert",
                    "severity": sev_from_mm(max_mm),
                    "location": {"lat": c["lat"], "lon": c["lon"]},
                    "message": f"{c['name']}: {round(max_mm,1)}mm around {max_t}",
                    "timestamp": now_ist
                })
    except:
        pass

    try:
        eq = requests.get(
            "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson",
            timeout=6
        ).json()
        for f in eq.get("features", []):
            lon, lat = f["geometry"]["coordinates"][0], f["geometry"]["coordinates"][1]
            if 6 <= lat <= 38 and 68 <= lon <= 98:
                mag = f["properties"]["mag"] or 0
                alerts.append({
                    "id": f["id"],
                    "type": "Earthquake",
                    "severity": "High" if mag >= 5 else "Medium" if mag >= 3 else "Low",
                    "location": {"lat": lat, "lon": lon},
                    "message": f"M{mag} near {f['properties'].get('place','')}",
                    "timestamp": now_ist
                })
    except:
        pass

    return {"status": "success", "count": len(alerts), "data": alerts}
