import geopandas as gpd
import osmnx as ox
from shapely.geometry import Point
import json
import os
import time
import concurrent.futures

from requests.exceptions import RequestException

_parcels_cache = None

def load_parcels():
    global _parcels_cache
    if _parcels_cache is None:
        print("📦 Loading Parcels.geojson...")
        _parcels_cache = gpd.read_file("Parcels.geojson").to_crs(epsg=4326)
    return _parcels_cache

# Load or create persistent cache
CACHE_PATH = "sidewalk_cache.json"
if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, "r") as f:
        _sidewalk_cache = json.load(f)
else:
    _sidewalk_cache = {}

def check_sidewalk_nearby(lat, lon, radius_m=50, timeout=8):
    key = f"{round(lat, 6)},{round(lon, 6)}"
    if key in _sidewalk_cache:
        return _sidewalk_cache[key]

    def fetch():
        tags = {"footway": "sidewalk"}
        return not ox.features_from_point((lat, lon), tags=tags, dist=radius_m).empty

    try:
        print(f"⏳ Checking {key}...")
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(fetch)
            result = future.result(timeout=timeout)
        duration = round(time.time() - start, 2)
        print(f"✅ Finished {key} in {duration}s → {result}")
    except concurrent.futures.TimeoutError:
        print(f"⏰ Timeout at {key} after {timeout}s")
        result = False
    except Exception as e:
        print(f"❌ Error at {key}: {e}")
        result = False

    _sidewalk_cache[key] = result

    if len(_sidewalk_cache) % 10 == 0:
        with open(CACHE_PATH, "w") as f:
            json.dump(_sidewalk_cache, f)

    return result

def get_features_from_point(lat, lon):
    parcels = load_parcels()
    point = Point(lon, lat)
    match = parcels[parcels.geometry.contains(point)]

    if match.empty:
        return {"error": "No parcel found at this location."}

    parcel = match.iloc[0]

    features = {
        "legalAcreage": parcel.get("legalAcreage", 0),
        "imprvActualYearBuilt": parcel.get("imprvActualYearBuilt", 0),
        "improvementValue": parcel.get("improvementValue", 0),
        "propType": str(parcel.get("propType", "Unknown")),
        "situs_city": str(parcel.get("situs_city", "Unknown")),
        "compactness": (parcel["ShapeSTLength"] ** 2) / parcel["ShapeSTArea"],
        "has_sidewalk": check_sidewalk_nearby(lat, lon)  # 👈 NEW FEATURE
    }

    return features
