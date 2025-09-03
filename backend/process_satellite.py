import rasterio
import numpy as np
import json
from rasterio.features import shapes

def compute_index(band1_path, band2_path, index="NDVI"):
    with rasterio.open(band1_path) as b1, rasterio.open(band2_path) as b2:
        band1 = b1.read(1).astype("float32")
        band2 = b2.read(1).astype("float32")
        profile = b1.profile
    if index == "NDVI":
        return (band2 - band1) / (band2 + band1 + 1e-6), profile
    elif index == "NDWI":
        return (band1 - band2) / (band1 + band2 + 1e-6), profile
    else:
        raise ValueError("Unknown index")

def raster_to_geojson(mask, transform, threshold=0.2):
    results = (
        {"properties": {"class": int(v)}, "geometry": s}
        for s, v in shapes(mask.astype("uint8"), transform=transform)
    )
    features = [r for r in results if r["properties"]["class"] == 1]
    return {"type": "FeatureCollection", "features": features}

if __name__ == "__main__":
    # Example: NDVI (Red=B04, NIR=B08)
    ndvi, profile = compute_index("../data/2025-08-19-00:00_2025-08-19-23:59_Sentinel-2_L1C_B04_(Raw).tiff", "../data/2025-08-19-00:00_2025-08-19-23:59_Sentinel-2_L1C_B05_(Raw).tiff", index="NDVI")
    ndvi_mask = ndvi > 0.3  # vegetation threshold
    ndvi_geojson = raster_to_geojson(ndvi_mask, profile["transform"])
    with open("../data/veg.geojson", "w") as f:
        json.dump(ndvi_geojson, f)

    # Example: NDWI (Green=B03, NIR=B08)
    ndwi, profile = compute_index("../data/2025-08-19-00:00_2025-08-19-23:59_Sentinel-2_L1C_B03_(Raw).tiff", "../data/2025-08-19-00:00_2025-08-19-23:59_Sentinel-2_L1C_B05_(Raw).tiff", index="NDWI")
    ndwi_mask = ndwi > 0.2  # water threshold
    ndwi_geojson = raster_to_geojson(ndwi_mask, profile["transform"])
    with open("../data/water.geojson", "w") as f:
        json.dump(ndwi_geojson, f)

    print("GeoJSONs generated: veg.geojson & water.geojson")
