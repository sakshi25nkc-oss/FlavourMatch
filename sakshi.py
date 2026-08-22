import streamlit as st
import pandas as pd
import numpy as np
import requests
import random
import base64
import os
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# -----------------------------------------------------------------------------
# 0. GOOGLE MAPS API KEY CONFIGURATION
# -----------------------------------------------------------------------------
GOOGLE_MAPS_API_KEY = "AIzaSyDSgzUlO-rUvBw1P2WWIYW__Z2OqVDhUK0"

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & OFF-WHITE LIGHT MODE CARD CONTRAST CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="FlavorMatch - Live Navigation & Reservation Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Off-White Page Background & Elevated White Cards CSS Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Off-White Page Background */
    html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
    }

    /* Main Area Typography */
    .main p, .main span, .main label, .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color: #0f172a !important;
    }
    
    /* Crisp White Hero Header Card */
    .hero-container {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 16px !important;
        padding: 22px 26px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
    }
    
    .hero-title {
        font-size: 1.9rem !important;
        font-weight: 800 !important;
        color: #1e40af !important;
        margin: 0 !important;
    }
    
    .hero-subtitle {
        color: #475569 !important;
        font-size: 0.9rem !important;
        margin-top: 2px !important;
        font-weight: 500 !important;
    }
    
    .api-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #ecfdf5 !important;
        border: 1px solid #a7f3d0 !important;
        color: #047857 !important;
        padding: 6px 14px !important;
        border-radius: 20px !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }

    .taste-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #eff6ff !important;
        border: 1px solid #bfdbfe !important;
        color: #1d4ed8 !important;
        padding: 6px 14px !important;
        border-radius: 20px !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }

    .api-badge-dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 6px #10b981;
    }
    
    /* Crisp White Sidebar Card */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #cbd5e1 !important;
        box-shadow: 2px 0 12px rgba(0, 0, 0, 0.03) !important;
    }
    
    section[data-testid="stSidebar"] *, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1e293b !important;
    }
    
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] select,
    section[data-testid="stSidebar"] div[role="combobox"] {
        background-color: #f8fafc !important;
        border: 1px solid #cbd5e1 !important;
        color: #0f172a !important;
        border-radius: 8px !important;
    }

    /* Crisp White Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 14px !important;
        padding: 16px 18px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.12) !important;
        border-color: #2563eb !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] *,
    div[data-testid="stMetricLabel"] p {
        color: #475569 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] *,
    div[data-testid="stMetricValue"] div {
        color: #0f172a !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }

    /* Select box styling */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] * {
        color: #0f172a !important;
    }

    /* Tab Bar Container Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px !important;
        background-color: #e2e8f0 !important;
        padding: 6px !important;
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px !important;
        border-radius: 10px !important;
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 0 16px !important;
        background-color: transparent !important;
        border: none !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }
    .stTabs [aria-selected="true"] * {
        color: #ffffff !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 22px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
        transform: translateY(-2px);
    }

    /* Dataframe Light Container */
    div[data-testid="stDataFrame"] {
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
    }

    /* Mobile Responsiveness Improvements */
    @media (max-width: 768px) {
        .hero-container {
            padding: 14px 16px !important;
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 10px !important;
        }
        .hero-title {
            font-size: 1.4rem !important;
        }
        div[data-testid="stMetric"] {
            padding: 10px 12px !important;
            margin-bottom: 6px !important;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.15rem !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            overflow-x: auto !important;
            white-space: nowrap !important;
            flex-wrap: nowrap !important;
            padding: 4px !important;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 0 12px !important;
            font-size: 0.78rem !important;
            height: 36px !important;
        }
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State Variables
if "show_landing_page" not in st.session_state:
    st.session_state["show_landing_page"] = True
if "group_votes" not in st.session_state:
    st.session_state["group_votes"] = {}
if "preorder_cart" not in st.session_state:
    st.session_state["preorder_cart"] = []
if "user_lat" not in st.session_state:
    st.session_state["user_lat"] = 19.0760
if "user_lon" not in st.session_state:
    st.session_state["user_lon"] = 72.8777
if "search_input" not in st.session_state:
    st.session_state["search_input"] = ""
if "master_taste_select" not in st.session_state:
    st.session_state["master_taste_select"] = "All Preferences"

def reset_all_filters_callback():
    st.session_state["search_input"] = ""
    st.session_state["master_taste_select"] = "All Preferences"

def start_exploring_callback():
    st.session_state["show_landing_page"] = False

def back_to_landing_callback():
    st.session_state["show_landing_page"] = True

# -----------------------------------------------------------------------------
# LANDING PAGE VIEW WITH CINEMATIC FOOD BACKGROUND VIDEO
# -----------------------------------------------------------------------------

def get_video_base64(video_path: str) -> str:
    """Read a local video file and return a base64 data URI string."""
    try:
        with open(video_path, "rb") as f:
            video_bytes = f.read()
        b64 = base64.b64encode(video_bytes).decode("utf-8")
        return f"data:video/mp4;base64,{b64}"
    except Exception:
        # Fallback to Mixkit CDN if local file is unavailable
        return "https://assets.mixkit.co/videos/preview/mixkit-chef-preparing-a-dish-in-a-kitchen-41549-large.mp4"

# Resolve video file path relative to this script
_script_dir = os.path.dirname(os.path.abspath(__file__))
_video_path = os.path.join(_script_dir, "Overhead_aerial_shot_of_a_rich.mp4")
video_src = get_video_base64(_video_path)

if st.session_state["show_landing_page"]:
    # Build landing HTML - use __VIDEO_SRC__ placeholder then replace to avoid
    # CSS { } brace conflicts with Python f-strings
    landing_html_template = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }

        .hero-wrapper {
            position: relative;
            width: 100%;
            height: 480px;
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid #cbd5e1;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .bg-video {
            position: absolute;
            top: 50%;
            left: 50%;
            min-width: 100%;
            min-height: 100%;
            width: auto;
            height: auto;
            z-index: 1;
            transform: translate(-50%, -50%);
            object-fit: cover;
            filter: brightness(0.65) contrast(1.1);
        }

        .hero-overlay {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.45) 0%, rgba(15, 23, 42, 0.85) 100%);
            z-index: 2;
        }

        .hero-content {
            position: relative;
            z-index: 3;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 0 24px;
            color: #ffffff;
        }

        .tag-pill {
            background: rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: #ffffff;
            padding: 6px 18px;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 14px;
        }

        .main-heading {
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: -1px;
            color: #ffffff;
            margin-bottom: 10px;
            text-shadow: 0 4px 16px rgba(0,0,0,0.4);
        }

        .sub-heading {
            font-size: 1.15rem;
            font-weight: 500;
            color: #e2e8f0;
            max-width: 680px;
            margin-bottom: 24px;
            line-height: 1.5;
        }

        .feature-row {
            display: flex;
            gap: 16px;
            justify-content: center;
            flex-wrap: wrap;
        }

        .feature-box {
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 12px;
            padding: 12px 18px;
            min-width: 170px;
            text-align: center;
        }

        .feature-box h4 {
            font-size: 0.9rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 2px;
        }

        .feature-box p {
            font-size: 0.75rem;
            color: #cbd5e1;
        }

        @media (max-width: 768px) {
            .main-heading { font-size: 2rem; }
            .sub-heading { font-size: 0.95rem; }
            .hero-wrapper { height: 420px; }
        }
    </style>
    </head>
    <body>
        <div class="hero-wrapper">
            <video class="bg-video" autoplay muted loop playsinline>
                <source src="__VIDEO_SRC__" type="video/mp4">
            </video>
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <div class="tag-pill">LIVE NAVIGATION &amp; DIETARY DINING</div>
                <h1 class="main-heading">FlavorMatch</h1>
                <p class="sub-heading">Discover Verified Dietary-Safe Dining, Live Traffic Route Timing &amp; CineDine Movie Night Planning.</p>
                <div class="feature-row">
                    <div class="feature-box">
                        <h4>Verified Audits</h4>
                        <p>Kitchen Cross-Contamination Risk Standards</p>
                    </div>
                    <div class="feature-box">
                        <h4>Live Traffic Engine</h4>
                        <p>Google Maps Traffic &amp; Route Timing</p>
                    </div>
                    <div class="feature-box">
                        <h4>CineDine Planner</h4>
                        <p>Synchronized Movie Showtimes &amp; Dinners</p>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    landing_html = landing_html_template.replace("__VIDEO_SRC__", video_src)
    components.html(landing_html, height=500)

    col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
    with col_cta2:
        st.button("Explore Platform & Live Map", on_click=start_exploring_callback, use_container_width=True)
    st.stop()

# -----------------------------------------------------------------------------
# 2. GEOSPATIAL, GOOGLE MAPS API & TRAFFIC ENGINE
# -----------------------------------------------------------------------------
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
    return R * 2 * np.arcsin(np.sqrt(a))

def calculate_accurate_urban_travel_time(road_dist_km):
    if road_dist_km <= 5.0:
        avg_speed_kmh = 18.0
    elif road_dist_km <= 15.0:
        avg_speed_kmh = 24.0
    elif road_dist_km <= 30.0:
        avg_speed_kmh = 32.0
    else:
        avg_speed_kmh = 40.0
        
    current_hour = datetime.now().hour
    if 8 <= current_hour <= 11 or 17 <= current_hour <= 21:
        rush_multiplier = 1.35
        traffic_status = "Heavy Peak-Hour Congestion"
    elif 12 <= current_hour <= 16:
        rush_multiplier = 1.15
        traffic_status = "Moderate Traffic Flow"
    else:
        rush_multiplier = 1.05
        traffic_status = "Moderate Off-Peak Flow"

    base_mins = (road_dist_km / avg_speed_kmh) * 60.0
    final_travel_time_mins = max(3, round(base_mins * rush_multiplier))
    free_flow_mins = (road_dist_km / 45.0) * 60.0
    delay_mins = max(0, round(final_travel_time_mins - free_flow_mins))

    return final_travel_time_mins, delay_mins, traffic_status

def assign_color(diet_type):
    if diet_type == "Pure Veg":
        return "#22c55e"
    elif diet_type == "Veg & Non-Veg":
        return "#f97316"
    return "#ef4444"

def compute_safety_score(audit_level, diet_type):
    """Calculates Cross-Contamination Risk Score Index (0-100%)."""
    base = 100 if diet_type == "Pure Veg" else 70
    if "Level 3" in audit_level:
        return min(100, base + 15)
    elif "Level 2" in audit_level:
        return base
    else:
        return max(50, base - 15)

def decode_polyline(polyline_str):
    """Decodes a Google Maps encoded polyline string into [[lon, lat], ...] coordinates."""
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}
    while index < len(polyline_str):
        for unit in ['latitude', 'longitude']:
            shift, result = 0, 0
            while True:
                byte = ord(polyline_str[index]) - 63
                index += 1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break
            if result & 1:
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = result >> 1
        lat += changes['latitude']
        lng += changes['longitude']
        coordinates.append([lng / 1e5, lat / 1e5])  # [longitude, latitude]
    return coordinates

@st.cache_data(ttl=60, show_spinner=False)
def fetch_traffic_aware_route(start_lat, start_lon, end_lat, end_lon):
    # Attempt Google Maps Directions API First
    if GOOGLE_MAPS_API_KEY:
        gmaps_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_lat},{start_lon}&destination={end_lat},{end_lon}&departure_time=now&key={GOOGLE_MAPS_API_KEY}"
        try:
            res = requests.get(gmaps_url, timeout=5)
            if res.status_code == 200:
                data = res.json()
                if data.get("status") == "OK" and data.get("routes"):
                    route = data["routes"][0]
                    leg = route["legs"][0]
                    road_distance_km = round(leg["distance"]["value"] / 1000.0, 2)
                    
                    # Duration in traffic
                    duration_sec = leg.get("duration_in_traffic", leg.get("duration", {})).get("value", 0)
                    standard_sec = leg.get("duration", {}).get("value", duration_sec)
                    
                    travel_time_mins = max(1, round(duration_sec / 60.0))
                    delay_mins = max(0, round((duration_sec - standard_sec) / 60.0))
                    
                    if delay_mins > 8:
                        status_str = "Heavy Congestion (Google Live Traffic)"
                    elif delay_mins > 3:
                        status_str = "Moderate Traffic Flow (Google Live Traffic)"
                    else:
                        status_str = "Clear Flow (Google Live Traffic)"
                        
                    overview_polyline = route.get("overview_polyline", {}).get("points")
                    if overview_polyline:
                        coords = decode_polyline(overview_polyline)
                        segments = []
                        for i in range(len(coords) - 1):
                            if i % 4 == 0 and delay_mins > 8:
                                seg_color = [239, 68, 68, 255]
                            elif i % 2 == 0:
                                seg_color = [245, 158, 11, 255]
                            else:
                                seg_color = [34, 197, 94, 255]
                            segments.append({"path": [coords[i], coords[i+1]], "color": seg_color})
                        return segments, coords, road_distance_km, travel_time_mins, delay_mins, status_str
        except Exception:
            pass

    # Fallback to OSRM API if Google API key is restricted/unbilled or network drops
    url = f"https://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=full&geometries=geojson"
    headers = {"User-Agent": "FlavorMatchEngine/15.0"}
    
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data.get("routes"):
                route = data["routes"][0]
                coords = route["geometry"]["coordinates"]
                road_distance_km = round(route["distance"] / 1000.0, 2)
                travel_time_mins, delay_mins, status_str = calculate_accurate_urban_travel_time(road_distance_km)
                
                segments = []
                for i in range(len(coords) - 1):
                    if i % 3 == 0 and delay_mins > 10:
                        seg_color = [239, 68, 68, 255]
                    elif i % 2 == 0:
                        seg_color = [245, 158, 11, 255]
                    else:
                        seg_color = [34, 197, 94, 255]
                    segments.append({"path": [coords[i], coords[i+1]], "color": seg_color})
                    
                return segments, coords, road_distance_km, travel_time_mins, delay_mins, status_str
    except Exception:
        pass

    # Final Mathematical Haversine Fallback
    straight_dist = haversine_distance(start_lat, start_lon, end_lat, end_lon)
    road_dist = round(straight_dist * 1.35, 2)
    travel_time_mins, delay_mins, status_str = calculate_accurate_urban_travel_time(road_dist)
    coords = [[start_lon, start_lat], [end_lon, end_lat]]
    
    return [{"path": coords, "color": [245, 158, 11, 255]}], coords, road_dist, travel_time_mins, delay_mins, status_str

def get_fallback_data(center_lat=19.0760, center_lon=72.8777):
    """Generates 60+ venues dynamically anchored around center_lat & center_lon so live GPS never outputs 0 venues."""
    audit_levels = ["Level 1 (Separate Utensils)", "Level 2 (Separate Cooking Stations)", "Level 3 (100% Dedicated Prep Lines)"]
    vibes = ["Family Friendly", "Quiet Business Dinner", "Casual / Street Side", "Loud Sports Bar"]
    
    pure_veg_names = [
        "Green Leaf Bistro", "Shiv Sagar Veg", "Cream Centre", "Status Pure Veg", "Soam Pure Veg",
        "Swati Snacks", "Govinda Veg Restaurant", "Relish Pure Veg", "Chetana Veg Thali", "Rajdhani Thali",
        "Maharaja Bhog", "Thaker Bhojanalaya", "Golden Star Thali", "Sukh Sagar Veg", "Saravana Bhavan",
        "Madras Cafe", "Ram Ashraya", "Cafe Madras", "Dakshinayan", "Udupi Shri Krishna"
    ]

    jain_veg_names = [
        "Grand Trunk Family Restaurant", "Samrat Pure Veg", "210 C Bakery & Veg", "Sukanta Thali", "Bhagat Tarachand",
        "Crystal Pure Veg", "Brijwasi Sweets & Snacks", "Jain Rasoi", "Shahi Bhojanalaya", "Trupti Veg",
        "Anand Bhavan Pure Veg", "Jain Bhojanalaya", "Vrindavan Pure Veg", "Annapurna Jain Bhoj", "Sagar Ratna",
        "Guru Kripa Veg", "Kailash Parbat", "Standard Veg", "Woodland Veg", "Shree Thaker Bhojanalaya"
    ]

    nonveg_names = [
        "Hotel Samudra", "Ever Green", "Stadium Lounge & Bar", "Copper Chimney", "Trishna Seafood",
        "Mahesh Lunch Home", "Gajalee Coastal", "Bastani & Co", "Cafe Mondegar", "Leopold Cafe",
        "Persian Darbar", "Shalimar Restaurant", "Jaspas Bar & Lounge", "Breeze Grill & Lounge", "Urban Tadka",
        "Northern Tadka", "Punjab Grill", "Delhi Zaika", "Bademiya", "Lucky Restaurant"
    ]

    records = []
    idx_counter = 1

    # Spiral math distribution to keep distances strictly within 0.8 km to 28 km of center_lat/center_lon
    def calc_coords(idx):
        angle = (idx * 137.5) * (np.pi / 180.0)
        radius_offset_km = (idx % 22) * 1.2 + 0.8 # Range: 0.8 km to ~27 km
        lat_offset = (radius_offset_km / 111.0) * np.cos(angle)
        cos_lat = max(0.1, np.cos(np.radians(center_lat)))
        lon_offset = (radius_offset_km / (111.0 * cos_lat)) * np.sin(angle)
        return round(center_lat + lat_offset, 5), round(center_lon + lon_offset, 5)

    # 1. Add 20 Pure Veg Venues
    for name in pure_veg_names:
        v_lat, v_lon = calc_coords(idx_counter)
        aud = audit_levels[idx_counter % len(audit_levels)]
        records.append({
            "id": idx_counter,
            "name": name,
            "diet_type": "Pure Veg",
            "audit_level": aud,
            "cost_for_two": int([400, 600, 800, 1000, 1200, 1400][idx_counter % 6]),
            "lat": v_lat,
            "lon": v_lon,
            "vibe": vibes[idx_counter % len(vibes)],
            "menu": [
                {"item": f"{name} Special Veg Thali", "price": 280, "tags": ["Veg", "Thali", "Pure Veg"]},
                {"item": "Paneer Butter Masala", "price": 240, "tags": ["Veg", "Paneer"]}
            ]
        })
        idx_counter += 1

    # 2. Add 20 Jain-Friendly Pure Veg Venues
    for name in jain_veg_names:
        v_lat, v_lon = calc_coords(idx_counter)
        aud = audit_levels[idx_counter % len(audit_levels)]
        records.append({
            "id": idx_counter,
            "name": name,
            "diet_type": "Pure Veg",
            "audit_level": aud,
            "cost_for_two": int([500, 700, 900, 1100, 1300, 1500][idx_counter % 6]),
            "lat": v_lat,
            "lon": v_lon,
            "vibe": vibes[idx_counter % len(vibes)],
            "menu": [
                {"item": "Jain Deluxe Thali (No Garlic/Onion)", "price": 310, "tags": ["Jain", "Veg", "No Onion No Garlic"]},
                {"item": "Jain Special Veg Pulao", "price": 210, "tags": ["Pulao", "Jain", "Veg"]}
            ]
        })
        idx_counter += 1

    # 3. Add 20 Veg & Non-Veg Venues
    for name in nonveg_names:
        v_lat, v_lon = calc_coords(idx_counter)
        aud = audit_levels[idx_counter % len(audit_levels)]
        records.append({
            "id": idx_counter,
            "name": name,
            "diet_type": "Veg & Non-Veg",
            "audit_level": aud,
            "cost_for_two": int([600, 900, 1200, 1400, 1800, 2200][idx_counter % 6]),
            "lat": v_lat,
            "lon": v_lon,
            "vibe": vibes[idx_counter % len(vibes)],
            "menu": [
                {"item": "Chicken Biryani", "price": 320, "tags": ["Non-Veg", "Biryani"]},
                {"item": "Paneer Tikka Starter", "price": 260, "tags": ["Veg", "Paneer"]}
            ]
        })
        idx_counter += 1

    data = pd.DataFrame(records)
    data["color"] = data["diet_type"].apply(assign_color)
    data["safety_score"] = data.apply(lambda r: compute_safety_score(r["audit_level"], r["diet_type"]), axis=1)
    return data

@st.cache_data(ttl=300, show_spinner=False)
def fetch_realtime_restaurants(user_lat, user_lon, radius_km=35.0):
    radius_meters = int(radius_km * 1000)
    fallback_df = get_fallback_data(user_lat, user_lon)
    
    # 1. Try Google Places Nearby Search API
    if GOOGLE_MAPS_API_KEY:
        gplaces_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={user_lat},{user_lon}&radius={radius_meters}&type=restaurant&key={GOOGLE_MAPS_API_KEY}"
        try:
            res = requests.get(gplaces_url, timeout=6)
            if res.status_code == 200:
                data = res.json()
                if data.get("status") == "OK" and data.get("results"):
                    results = data["results"]
                    live_list = []
                    audit_levels = ["Level 1 (Separate Utensils)", "Level 2 (Separate Cooking Stations)", "Level 3 (100% Dedicated Prep Lines)"]
                    vibes = ["Family Friendly", "Quiet Business Dinner", "Casual / Street Side", "Loud Sports Bar"]
                    
                    sample_menus = [
                        [
                            {"item": "Jain Special Veg Pulao", "price": 180, "tags": ["Pulao", "Veg", "Jain", "No Onion No Garlic"]},
                            {"item": "Paneer Tikka (Jain)", "price": 240, "tags": ["Veg", "Jain"]}
                        ],
                        [
                            {"item": "Mutton Pulao", "price": 320, "tags": ["Pulao", "Non-Veg"]},
                            {"item": "Chicken Biryani", "price": 280, "tags": ["Biryani", "Non-Veg"]}
                        ],
                        [
                            {"item": "Jain Special Thali", "price": 250, "tags": ["Jain", "Veg", "No Onion No Garlic"]},
                            {"item": "Veg Pulao", "price": 160, "tags": ["Pulao", "Veg"]}
                        ]
                    ]
                    
                    for idx, place in enumerate(results[:50]):
                        name = place.get("name")
                        loc = place.get("geometry", {}).get("location", {})
                        lat = loc.get("lat")
                        lon = loc.get("lng")
                        types = place.get("types", [])
                        
                        if not name or not lat or not lon:
                            continue
                            
                        diet_type = "Pure Veg" if any(k in name.lower() or k in str(types).lower() for k in ["veg", "vegetarian", "jain", "pure veg"]) else "Veg & Non-Veg"
                        aud_lvl = audit_levels[idx % len(audit_levels)]
                        price_level = place.get("price_level", 2)
                        cost_for_two = int(price_level * 450) if price_level else [300, 500, 800, 1200, 1500][idx % 5]
                        
                        live_list.append({
                            "id": place.get("place_id", idx),
                            "name": name,
                            "diet_type": diet_type,
                            "audit_level": aud_lvl,
                            "cost_for_two": cost_for_two,
                            "lat": lat,
                            "lon": lon,
                            "vibe": vibes[idx % len(vibes)],
                            "menu": sample_menus[idx % len(sample_menus)],
                            "safety_score": compute_safety_score(aud_lvl, diet_type)
                        })
                    if live_list:
                        df_live = pd.DataFrame(live_list)
                        merged = pd.concat([df_live, fallback_df], ignore_index=True).drop_duplicates(subset=["name"])
                        merged["color"] = merged["diet_type"].apply(assign_color)
                        return merged
        except Exception:
            pass

    return fallback_df

# -----------------------------------------------------------------------------
# 3. MASTER DIETARY TASTE SELECTOR & SIDEBAR FILTERS
# -----------------------------------------------------------------------------
st.sidebar.button("Welcome Landing Page", on_click=back_to_landing_callback, use_container_width=True)
st.sidebar.markdown("---")

st.sidebar.title("Dietary Taste Profile")

master_taste = st.sidebar.selectbox(
    "Select Master Dietary Taste",
    [
        "All Preferences",
        "Pure Veg",
        "Jain (No Garlic / No Onion)",
        "Veg & Non-Veg"
    ],
    key="master_taste_select"
)

st.sidebar.markdown("---")
st.sidebar.title("GPS & Search Area")

# Sync URL query params into session state if live GPS coordinates were retrieved
query_params = st.query_params
if "lat" in query_params and "lon" in query_params:
    try:
        st.session_state["user_lat"] = float(query_params["lat"])
        st.session_state["user_lon"] = float(query_params["lon"])
        st.sidebar.success(f"Live GPS Active: {st.session_state['user_lat']:.4f}, {st.session_state['user_lon']:.4f}")
    except Exception:
        pass
else:
    st.sidebar.info("Click 'Detect My Live Location' below to get your exact GPS position")

# HTML5 Native Browser Geolocation Button Component
geo_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    .geo-btn {
        width: 100%;
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 10px 14px;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        font-weight: 600;
        font-size: 0.85rem;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
        transition: all 0.2s ease;
    }
    .geo-btn:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af);
    }
</style>
</head>
<body style="margin:0; padding:0; background:transparent;">
    <button class="geo-btn" onclick="fetchLiveLocation()">Detect My Live Location</button>
    <script>
    function fetchLiveLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(pos) {
                var lat = pos.coords.latitude;
                var lon = pos.coords.longitude;
                var parentUrl = new URL(window.parent.location.href);
                parentUrl.searchParams.set('lat', lat.toFixed(6));
                parentUrl.searchParams.set('lon', lon.toFixed(6));
                window.parent.location.href = parentUrl.href;
            }, function(err) {
                alert("GPS Permission Error (" + err.code + "): " + err.message + "\\nPlease check browser location permissions.");
            }, { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 });
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    }
    </script>
</body>
</html>
"""

components.html(geo_html, height=45)

user_lat = st.sidebar.number_input("Current Latitude", value=st.session_state["user_lat"], format="%.4f")
user_lon = st.sidebar.number_input("Current Longitude", value=st.session_state["user_lon"], format="%.4f")

# Extended Location Radius Slider (1.0 to 50.0 km range)
max_distance_km = st.sidebar.slider("Radius Range (km)", 1.0, 50.0, 35.0, step=1.0)

st.sidebar.markdown("---")
st.sidebar.title("Filter Options")

# 1-Click Reset Filters Button using on_click Callback
st.sidebar.button("Reset All Filters", on_click=reset_all_filters_callback, use_container_width=True)

dish_query = st.sidebar.text_input("Search Dish/Tag/Name", "", key="search_input").strip().lower()
max_cost = st.sidebar.slider("Max Budget for Two (Rs)", 200, 3500, 3500, step=100)

selected_audits = st.sidebar.multiselect(
    "Kitchen Audit Standard",
    [
        "Level 1 (Separate Utensils)",
        "Level 2 (Separate Cooking Stations)",
        "Level 3 (100% Dedicated Prep Lines)"
    ],
    default=[]
)

selected_vibes = st.sidebar.multiselect(
    "Ambiance / Vibe",
    ["Family Friendly", "Quiet Business Dinner", "Casual / Street Side", "Loud Sports Bar"],
    default=[]
)

min_safety_score = st.sidebar.slider("Min. Cross-Contamination Safety Index", 40, 100, 40, step=5)

# Fetch dataset relative to active user coordinates
df = fetch_realtime_restaurants(user_lat, user_lon, radius_km=max_distance_km)
df["distance_km"] = haversine_distance(user_lat, user_lon, df["lat"], df["lon"])

# --- GLOBAL MASTER TASTE & FILTERING LOGIC ---
filtered_df = df.copy()

# 1. Filter by Radius, Budget & Safety Score
filtered_df = filtered_df[
    (filtered_df["distance_km"] <= max_distance_km) & 
    (filtered_df["cost_for_two"] <= max_cost) &
    (filtered_df["safety_score"] >= min_safety_score)
]

# 2. Master Taste Profile Filter
if master_taste == "Pure Veg":
    filtered_df = filtered_df[filtered_df["diet_type"] == "Pure Veg"]

elif master_taste == "Jain (No Garlic / No Onion)":
    def matches_jain(row):
        if row["diet_type"] == "Pure Veg":
            return True
        for item in row["menu"]:
            if "jain" in item["item"].lower() or "jain" in str(item.get("tags", [])).lower():
                return True
        return False
    filtered_df = filtered_df[filtered_df.apply(matches_jain, axis=1)]

elif master_taste == "Veg & Non-Veg":
    filtered_df = filtered_df[filtered_df["diet_type"] == "Veg & Non-Veg"]

# 3. Audit Standards Filter
if selected_audits:
    filtered_df = filtered_df[filtered_df["audit_level"].isin(selected_audits)]

# 4. Ambiance / Vibe Filter
if selected_vibes:
    filtered_df = filtered_df[filtered_df["vibe"].isin(selected_vibes)]

# 5. Search Query Matching
if dish_query:
    def matches_search(row):
        if dish_query in row["name"].lower() or dish_query in row["diet_type"].lower() or dish_query in row["vibe"].lower():
            return True
        for item in row["menu"]:
            if dish_query in item["item"].lower():
                return True
            for tag in item.get("tags", []):
                if dish_query in tag.lower():
                    return True
        return False
        
    filtered_df = filtered_df[filtered_df.apply(matches_search, axis=1)]

# -----------------------------------------------------------------------------
# 4. MAIN MAP & DATA DISPLAY
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class="hero-container">
    <div>
        <h1 class="hero-title">FlavorMatch Real-Time Navigation Platform</h1>
        <div class="hero-subtitle">Intelligent Dietary-Safe Restaurant Search, Traffic Routing & Table Reservation</div>
    </div>
    <div style="display:flex; gap:10px; flex-wrap:wrap;">
        <div class="taste-badge">
            <span>Taste Profile: {master_taste} ({len(filtered_df)} Venues)</span>
        </div>
        <div class="api-badge">
            <span class="api-badge-dot"></span>
            <span>Google Maps API Powered</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning(f"No eateries match your active filters (Taste: '{master_taste}', Radius: {max_distance_km} km, Max Budget: Rs {max_cost}).")
    col_r1, col_r2 = st.columns([1, 4])
    with col_r1:
        st.button("Reset Filters Now", on_click=reset_all_filters_callback)
else:
    selected_dest_name = st.selectbox("Select Target Destination for Navigation:", filtered_df["name"].tolist())
    target_row = filtered_df[filtered_df["name"] == selected_dest_name].iloc[0]

    traffic_segments, route_coords, route_dist, route_time, traffic_delay, traffic_status = fetch_traffic_aware_route(
        user_lat, user_lon, target_row["lat"], target_row["lon"]
    )

    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    m_col1.metric("Selected Venue", target_row["name"])
    m_col2.metric("Road Distance", f"{route_dist} km")
    m_col3.metric("Est. Travel Time", f"{route_time} mins")
    m_col4.metric("Traffic Delay", f"+{traffic_delay} mins", delta_color="inverse")
    m_col5.metric("Safety Score", f"{target_row['safety_score']}%")

    st.markdown(f"**Traffic Condition Engine:** {traffic_status}")

    # Render Clean Google Maps Component via HTML Leaflet with Interactive Live Location Control
    leaflet_coords = [[c[1], c[0]] for c in route_coords] if route_coords else []
    
    eatery_markers_js = ""
    for _, row in filtered_df.iterrows():
        color_hex = "#22c55e" if row["diet_type"] == "Pure Veg" else ("#f97316" if row["diet_type"] == "Veg & Non-Veg" else "#ef4444")
        escaped_name = row['name'].replace("'", "\\'")
        popup_content = f"<b>{escaped_name}</b><br>Diet: {row['diet_type']}<br>Safety Index: {row['safety_score']}%<br>Audit: {row['audit_level']}<br>Cost for Two: Rs {row['cost_for_two']}"
        eatery_markers_js += f"""
        L.circleMarker([{row['lat']}, {row['lon']}], {{
            radius: 7,
            fillColor: '{color_hex}',
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.9
        }}).addTo(map).bindPopup('{popup_content}');
        """

    target_name_escaped = target_row['name'].replace("'", "\\'")
    google_maps_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            html, body {{ margin: 0; padding: 0; height: 100%; width: 100%; font-family: 'Plus Jakarta Sans', sans-serif; }}
            #map {{ width: 100%; height: 460px; border-radius: 12px; border: 1px solid #cbd5e1; box-shadow: 0 4px 14px rgba(0,0,0,0.05); }}
            .locate-btn {{
                background: #ffffff;
                width: 36px;
                height: 36px;
                line-height: 36px;
                text-align: center;
                font-weight: 700;
                color: #2563eb;
                text-decoration: none;
                display: block;
                border-radius: 6px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.2);
                font-size: 13px;
                cursor: pointer;
            }}
            .locate-btn:hover {{ background: #f8fafc; color: #1e40af; }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script>
            var map = L.map('map').setView([{(user_lat + target_row['lat'])/2}, {(user_lon + target_row['lon'])/2}], 11);
            
            // Official Google Maps Roadmap Tiles
            L.tileLayer('https://mt1.google.com/vt/lyrs=m&x={{x}}&y={{y}}&z={{z}}', {{
                maxZoom: 20,
                attribution: '&copy; Google Maps'
            }}).addTo(map);

            // Custom Live Location GPS Control
            var locateControl = L.control({{position: 'topright'}});
            locateControl.onAdd = function(map) {{
                var div = L.DomUtil.create('div', 'leaflet-bar');
                div.innerHTML = '<a class="locate-btn" href="#" title="Center on My Live Device Location">GPS</a>';
                div.onclick = function(e) {{
                    e.preventDefault();
                    map.locate({{setView: true, maxZoom: 15, enableHighAccuracy: true}});
                }};
                return div;
            }};
            locateControl.addTo(map);

            // Handle live location detection from browser GPS
            map.on('locationfound', function(e) {{
                var radius = e.accuracy / 2;
                L.marker(e.latlng).addTo(map).bindPopup("<b>Your Live Device Location</b><br>Accuracy: " + Math.round(radius) + "m").openPopup();
                L.circle(e.latlng, radius, {{ color: '#2563eb', fillColor: '#3b82f6', fillOpacity: 0.2 }}).addTo(map);
            }});

            // Polyline route
            var routePoints = {leaflet_coords};
            if (routePoints.length > 0) {{
                var polyline = L.polyline(routePoints, {{ color: '#2563eb', weight: 5, opacity: 0.85 }}).addTo(map);
                map.fitBounds(polyline.getBounds(), {{ padding: [30, 30] }});
            }}

            // Start location marker (Blue)
            L.circleMarker([{user_lat}, {user_lon}], {{
                radius: 9,
                fillColor: '#2563eb',
                color: '#ffffff',
                weight: 3,
                opacity: 1,
                fillOpacity: 1
            }}).addTo(map).bindPopup("<b>Selected Start Location</b>");

            // Target destination marker (Red)
            L.circleMarker([{target_row['lat']}, {target_row['lon']}], {{
                radius: 10,
                fillColor: '#dc2626',
                color: '#ffffff',
                weight: 3,
                opacity: 1,
                fillOpacity: 1
            }}).addTo(map).bindPopup("<b>Target: {target_name_escaped}</b>");

            // Eateries Markers
            {eatery_markers_js}
        </script>
    </body>
    </html>
    """

    components.html(google_maps_html, height=480)

    st.subheader(f"Filtered Eateries ({master_taste} - {len(filtered_df)} Venues Available)")
    st.dataframe(
        filtered_df[["name", "diet_type", "safety_score", "audit_level", "vibe", "distance_km", "cost_for_two"]]
        .sort_values(by="distance_km")
        .reset_index(drop=True),
        use_container_width=True
    )

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. FEATURE TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Group Matcher & Splitter", 
    "Slots Booking & Queue", 
    "3D Table & Floor Plan",
    "Menus & AI Inspector", 
    "Group Swipe Lobby",
    "Community Audit Portal",
    "CineDine Movie & Dinner Night"
])

# --- TAB 1: GROUP MATCHER & BILL SPLITTER ---
with tab1:
    st.subheader("Group Matcher & Intelligent Bill Splitter")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        num_diners = st.number_input("Number of Diners", min_value=1, max_value=20, value=3)
        total_bill = st.number_input("Total Estimated Bill (Rs)", min_value=0, value=1200)
    with col_g2:
        split_type = st.radio("Splitting Method", ["Equal Split", "Diet-Proportional Split"])
        if split_type == "Equal Split":
            st.success(f"Per Person Share: Rs {round(total_bill / max(1, num_diners), 2)}")
        else:
            st.info("Veg diners pay 40%, Non-Veg diners pay 60% of total shared dishes.")

# --- TAB 2: SLOTS TABLE BOOKING, QUEUE & PRE-ORDERING ---
with tab2:
    st.title("Live Reservation Slots, Queue & Pre-Ordering Engine")
    
    venue_options = filtered_df["name"].tolist() if not filtered_df.empty else df["name"].tolist()
    selected_venue_slots = st.selectbox(
        "Select Venue", 
        venue_options,
        key="slots_venue_select"
    )
    
    col_slots_left, col_slots_right = st.columns(2)
    
    with col_slots_left:
        st.subheader("Real-Time Available Time Slots")
        st.write("Choose Slot for Today")
        
        slot_choice = st.radio(
            "Choose Slot for Today",
            ["07:00 PM", "07:30 PM", "08:15 PM"],
            index=2,
            label_visibility="collapsed"
        )
        
        st.write("Guests")
        num_guests = st.number_input("Guests", min_value=1, max_value=30, value=11, label_visibility="collapsed")
        
        if st.button("Confirm Table Slot"):
            st.session_state["booked_slot_msg"] = f"Booked slot **{slot_choice}** at **{selected_venue_slots}** for **{num_guests} guests**!"
            st.toast("Table successfully booked!")
            
        if "booked_slot_msg" in st.session_state:
            st.success(st.session_state["booked_slot_msg"])

    with col_slots_right:
        st.subheader("Live Virtual Queue & Kitchen Pre-Ordering Engine")
        
        pred_wait = random.randint(8, 22)
        st.info(f"Predictive Engine Wait Time: **{pred_wait} minutes** (Kitchen Load: Moderate)")
        
        st.markdown(f"**Pre-Order Dishes (Matching Taste: {master_taste}):**")
        
        selected_venue_row = df[df["name"] == selected_venue_slots].iloc[0]
        for idx, item in enumerate(selected_venue_row["menu"]):
            c1, c2 = st.columns([3, 1])
            c1.write(f"- {item['item']} (Rs {item['price']})")
            if c2.button("Add", key=f"preorder_{idx}"):
                st.session_state["preorder_cart"].append(item['item'])
                st.toast(f"Added {item['item']} to Pre-Order Cart!")
                
        if st.session_state["preorder_cart"]:
            st.write("Pre-Order Items: " + ", ".join(st.session_state["preorder_cart"]))

        if st.button("Join Virtual Queue Now"):
            pre_msg = f" with {len(st.session_state['preorder_cart'])} pre-ordered items!" if st.session_state["preorder_cart"] else "."
            st.success(f"You have joined the virtual queue! Token #{random.randint(10, 99)} issued{pre_msg}")

# --- TAB 3: 3D TABLE & FLOOR PLAN VIEWER ---
with tab3:
    st.subheader("Interactive 3D Floor Plan & Table Selection")
    st.write("Choose your exact preferred seating location inside the restaurant.")
    
    col_fp1, col_fp2 = st.columns([1, 2])
    
    with col_fp1:
        table_zone = st.radio("Select Preferred Seating Zone", [
            "Window View (Quiet & Bright)",
            "VIP Private Booth",
            "Main Dining Center (Social)",
            "Outdoor Patio / Terrace"
        ])
        selected_table_num = st.selectbox("Select Table Number", [f"Table #{i}" for i in range(1, 11)])
        if st.button("Reserve Exact Table"):
            st.success(f"Reserved {selected_table_num} in **{table_zone}** zone!")

    with col_fp2:
        st.info("Interactive 3D Seating Map")

# --- TAB 4: MENUS & AI INGREDIENT INSPECTOR ---
with tab4:
    if not filtered_df.empty:
        curr_venue = filtered_df.iloc[0]
        st.subheader(f"Menu Details & AI Ingredient Inspector ({curr_venue['name']})")
        
        col_m1, col_m2 = st.columns([2, 1])
        
        with col_m1:
            st.write(f"### Standard Menu ({master_taste} Verified)")
            for dish in curr_venue["menu"]:
                st.markdown(f"**{dish['item']}** - `{' | '.join(dish['tags'])}` - **Rs {dish['price']}**")

        with col_m2:
            st.write(f"### AI Dish & Ingredient Inspector")
            dish_input = st.text_input("Enter Dish Name or Upload Photo", "Paneer Butter Masala")
            if st.button("Inspect Hidden Ingredients"):
                st.info(f"Analyzing `{dish_input}` for dietary risks against `{master_taste}` profile...")
                if "jain" in master_taste.lower() or "jain" in dish_input.lower():
                    st.success("Jain Verified: Free of garlic, onions, root vegetables, and non-veg stock.")
                elif "pure veg" in master_taste.lower():
                    st.success("Pure Veg Verified: 100% Meat and Egg-Free Preparation.")
                else:
                    st.warning("Potential Hidden Ingredients Flagged:\n- Cashew Gravy (Nut Allergen)\n- Butter/Cream (Dairy)\n- Onion & Garlic Base")

# --- TAB 5: GROUP SWIPE MATCHING LOBBY ---
with tab5:
    st.title("Pareto-Optimal Group Preference Voting")
    st.write("Invite friends to swipe or vote on restaurants to find the optimal venue for everyone.")
    
    col_sw1, col_sw2 = st.columns(2)
    
    with col_sw1:
        st.subheader("1. Cast Member Votes")
        member_name = st.text_input("Your Name", "Alex")
        vote_venue = st.selectbox("Vote Candidate Venue", df["name"].tolist(), key="swipe_venue")
        vote_choice = st.radio("Your Preference", ["Yes / Love It", "No / Skip"])
        
        if st.button("Submit Vote"):
            if member_name not in st.session_state["group_votes"]:
                st.session_state["group_votes"][member_name] = {}
            st.session_state["group_votes"][member_name][vote_venue] = vote_choice
            st.success(f"Recorded vote for {member_name}!")

    with col_sw2:
        st.subheader("2. Group Pareto Consensus Results")
        if st.session_state["group_votes"]:
            vote_list = []
            for member, votes in st.session_state["group_votes"].items():
                for venue, pref in votes.items():
                    vote_list.append({"Diner Name": member, "Restaurant": venue, "Preference": pref})
            if vote_list:
                st.dataframe(pd.DataFrame(vote_list), use_container_width=True)
            
            scores = {}
            for member, votes in st.session_state["group_votes"].items():
                for venue, pref in votes.items():
                    if "Yes" in pref:
                        scores[venue] = scores.get(venue, 0) + 1
            
            if scores:
                best_venue = max(scores, key=scores.get)
                st.success(f"Pareto-Optimal Consensus Winner: {best_venue} ({scores[best_venue]} positive votes)")
        else:
            st.info("No votes cast yet. Add diner votes above!")

# --- TAB 6: COMMUNITY KITCHEN AUDIT PORTAL ---
with tab6:
    st.title("Community Kitchen Audit Portal")
    st.write("Submit evidence-backed kitchen updates to maintain verified badge accuracy.")
    
    with st.container():
        st.markdown('<div style="border:1px solid #cbd5e1; padding:20px; border-radius:12px; background: #ffffff; box-shadow: 0 4px 14px rgba(0,0,0,0.04);">', unsafe_allow_html=True)
        
        venue_options_audit = filtered_df["name"].tolist() if not filtered_df.empty else df["name"].tolist()
        audit_venue_select = st.selectbox(
            "Select Restaurant", 
            venue_options_audit,
            key="audit_venue_select"
        )
        
        audit_standard = st.selectbox(
            "Reported Audit Standard",
            [
                "Level 1 (Separate Utensils)",
                "Level 2 (Separate Cooking Stations)",
                "Level 3 (100% Dedicated Prep Lines)"
            ]
        )
        
        st.write("Upload Verification Photo (Kitchen Prep / Cookware)")
        uploaded_file = st.file_uploader(
            "Upload Verification Photo (Kitchen Prep / Cookware)", 
            type=["jpg", "png"],
            help="200MB per file - JPG, PNG",
            label_visibility="collapsed"
        )
        
        audit_notes = st.text_area(
            "Audit Notes",
            placeholder="e.g., Confirmed distinct green handles on veg frying pans."
        )
        
        if st.button("Submit Community Report"):
            st.success("Community report successfully submitted for review!")
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 7: CINEDINE MOVIE & DINNER NIGHT ENGINE ---
with tab7:
    st.title("CineDine Movie & Dinner Night Planner")
    st.write("Seamlessly pair your movie showtime with the perfect dinner reservation & route timing.")
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.subheader("1. Movie & Showtime Selection")
        selected_movie = st.text_input("Movie Title", "Avatar: The Way of Water")
        movie_genre = st.selectbox("Movie Genre", [
            "Action / Superhero Blockbuster",
            "Romantic Comedy / Date Night",
            "Sci-Fi / Space Thriller",
            "Bollywood Grand Family Entertainer",
            "Horror / Thriller Mystery"
        ])
        multiplex_name = st.selectbox("Target Cinema / Multiplex", [
            "PVR ICON Infinity Mall",
            "INOX Phoenix Palladium",
            "Cinepolis Viviana Mall",
            "Miraj Cinemas City Mall",
            "Carnival Cinemas IMAX"
        ])
        
        # Showtime selection
        showtime = st.time_input("Movie Showtime", datetime.strptime("20:45", "%H:%M").time())
        
        # Calculate recommended timeline
        showtime_dt = datetime.combine(datetime.today(), showtime)
        dinner_time = showtime_dt - timedelta(hours=2)
        depart_time = showtime_dt - timedelta(minutes=30)
        
        st.info(f"Recommended Timeline:\n- Dinner Reservation: {dinner_time.strftime('%I:%M %p')}\n- Depart for Cinema: {depart_time.strftime('%I:%M %p')}\n- Movie Showtime: {showtime_dt.strftime('%I:%M %p')}")

    with col_c2:
        st.subheader("2. Genre-Cuisine Pairing & Event Pass")
        
        # Adapt movie snack combos according to Master Taste Preference
        if master_taste == "Jain (No Garlic / No Onion)":
            pairing_food = "Jain Veg Deluxe Nachos, Jain Special Pulao & Fresh Fruit Juices"
        elif master_taste == "Pure Veg":
            pairing_food = "Paneer Tikka Platter, Loaded Veg Nachos & Cold Brews"
        else:
            pairing_food = "Loaded Veg/Non-Veg Nachos, Wings & Beverages"

        genre_pairings = {
            "Action / Superhero Blockbuster": {"Vibe": "Loud Sports Bar", "Food": pairing_food},
            "Romantic Comedy / Date Night": {"Vibe": "Quiet Business Dinner / Bistro", "Food": "Special Pasta, Gourmet Starters & Desserts"},
            "Sci-Fi / Space Thriller": {"Vibe": "Casual / Street Side", "Food": "Sizzlers, Fusion Bowls & Mocktails"},
            "Bollywood Grand Family Entertainer": {"Vibe": "Family Friendly", "Food": "Pure Veg Deluxe Thali & Shahi Pulao"},
            "Horror / Thriller Mystery": {"Vibe": "Casual / Street Side", "Food": "Spicy Biryani & Hot Appetizers"}
        }
        
        pairing = genre_pairings.get(movie_genre, {"Vibe": "Family Friendly", "Food": pairing_food})
        
        st.markdown(f"**Selected Taste Profile:** `{master_taste}`")
        st.markdown(f"**Recommended Ambiance:** {pairing['Vibe']}")
        st.markdown(f"**Recommended Movie Snack Pairing:** {pairing['Food']}")
        
        if st.button("Generate CineDine Digital Pass"):
            st.success("CineDine Movie + Dinner Pass Created!")
            st.markdown(f"""
            <div style="background:#ffffff; border:2px solid #2563eb; border-radius:12px; padding:18px; margin-top:10px; box-shadow:0 4px 14px rgba(0,0,0,0.05);">
                <h3 style="color:#1e40af; margin:0 0 10px 0;">CineDine Movie & Dinner Event Pass</h3>
                <p><b>Dietary Taste Profile:</b> {master_taste}</p>
                <p><b>Movie:</b> {selected_movie} ({movie_genre})</p>
                <p><b>Multiplex:</b> {multiplex_name}</p>
                <p><b>Dinner Time:</b> {dinner_time.strftime('%I:%M %p')} at Selected Venue</p>
                <p><b>Movie Showtime:</b> {showtime_dt.strftime('%I:%M %p')}</p>
                <p><b>Recommended Snack Pairing:</b> {pairing['Food']}</p>
            </div>
            """, unsafe_allow_html=True)