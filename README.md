# 🌍 DisasterGuard – AI-Powered Disaster Tracking & Alert System

## 📌 Overview
**DisasterGuard** is a real-time disaster tracking and alert platform designed to monitor, visualize, and provide timely warnings for natural disasters such as **floods, earthquakes, thunderstorms, and heavy rainfall**.  
The system aggregates **live data from multiple trusted APIs** and uses AI-powered analytics to assess severity, visualize impact zones, and deliver relevant alerts to end-users.

Our goal is to provide an **interactive, data-driven, and scalable platform** that can be deployed for community safety, research, and government use.

---

## 🎯 Key Features (Planned Goals)

### ✅ Phase 1 – Core Map & Alerts
- Real-time interactive **dark-mode map** using **Leaflet.js**.
- Display live disaster alerts with **animated concentric circles** indicating severity & impact radius.
- Filter disasters by type (**Rain, Flood, Thunderstorm, Earthquake**).
- Fetch live data from APIs such as:
  - **IMD** (Rainfall & Weather)
  - **USGS** (Earthquakes)
  - Other relevant open data sources.

### 🔜 Phase 2 – Advanced Integration
- Add **multi-disaster API aggregation** (combine weather, seismic, flood data).
- Real-time API updates without manual refresh.
- Mobile-responsive design.

### 🚀 Phase 3 – AI & Predictive Analytics
- Implement AI/ML to **predict disaster spread** based on historical & real-time data.
- Automated **risk scoring** for each event.
- Provide **localized alerts** based on user’s location.

---

## 🛠️ Tech Stack
**Frontend:**
- HTML5, CSS3, JavaScript (Vanilla)
- Leaflet.js (Map rendering)
- CARTO Basemaps

**Backend:**
- Python (FastAPI)
- Requests (API calls)
- Pytz (Time zone handling)

**Other Tools:**
- Uvicorn (ASGI Server)
- Git/GitHub for version control

---

## 📂 Project Structure
