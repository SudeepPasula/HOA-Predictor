import geopandas as gpd
import pandas as pd

# Load the parcel data and convert to WGS84
parcels = gpd.read_file("parcels.geojson").to_crs(epsg=4326)

# Apply heuristics to assign HOA or non-HOA labels
def compute_heuristic_features(row):
    try:
        compactness = (row["ShapeSTLength"] ** 2) / row["ShapeSTArea"]
    except:
        compactness = 0
    year = row.get("imprvActualYearBuilt", 0) or 0
    acreage = row.get("legalAcreage", 0) or 0

    if (
        year >= 2005 and
        acreage <= 0.3 and
        compactness <= 20
    ):
        return 1  # HOA
    elif (
        year <= 2000 and
        acreage >= 0.5 and
        compactness >= 25
    ):
        return 0  # Non-HOA
    else:
        return None

# Label parcels using heuristic
parcels["hoa_label"] = parcels.apply(compute_heuristic_features, axis=1)

# Keep only valid geometries with labels
labeled = parcels[parcels["hoa_label"].notnull()]
labeled = labeled[labeled.geometry.is_valid]

# Project to metric CRS for centroid calculation
projected = labeled.to_crs(epsg=3857)

# Calculate accurate centroid in meters, then convert back to WGS84 for lat/lon
labeled["latitude"] = projected.centroid.to_crs(epsg=4326).y
labeled["longitude"] = projected.centroid.to_crs(epsg=4326).x

# Select and clean features for training
df = labeled[[
    "hoa_label",
    "latitude", "longitude",
    "legalAcreage",
    "imprvActualYearBuilt",
    "ShapeSTLength",
    "ShapeSTArea",
    "improvementValue",
    "propType",
    "situs_city"
]].copy()

# Convert types and clean missing data
df = df.fillna(0)
df["propType"] = df["propType"].astype(str)
df["situs_city"] = df["situs_city"].astype(str)

# Compute compactness
df["compactness"] = (df["ShapeSTLength"] ** 2) / df["ShapeSTArea"]

# Save the cleaned and labeled training dataset
df.to_csv("hoa_training.csv", index=False)
print(f"✅ Saved {len(df)} labeled records to hoa_training.csv with lat/lon")
