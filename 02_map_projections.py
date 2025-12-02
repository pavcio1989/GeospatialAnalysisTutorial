import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt


# Load a GeoDataFrame containing regions in Ghana
regions = gpd.read_file("data/inputs/02/Regions/Map_of_Regions_in_Ghana.shp")
print(regions.crs)  # EPSG:32630 - Mercator projection

# Create a DataFrame with health facilities in Ghana
facilities_df = pd.read_csv("data/inputs/02/health_facilities.csv")

# Convert the DataFrame to a GeoDataFrame
facilities = gpd.GeoDataFrame(facilities_df, geometry=gpd.points_from_xy(facilities_df.Longitude, facilities_df.Latitude))

# Set the coordinate reference system (CRS) to EPSG 4326
facilities.crs = {'init': 'epsg:4326'}

# Create a map
ax = regions.plot(figsize=(8,8), color='whitesmoke', linestyle=':', edgecolor='black')
facilities.to_crs(epsg=32630).plot(markersize=1, ax=ax)
plt.show()

# The "Latitude" and "Longitude" columns are unchanged
print(facilities.to_crs(epsg=32630).head())

# Change the CRS to EPSG 4326
print(regions.to_crs("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs").head())

# Get the x-coordinate of each point
print(facilities.geometry.head().x)

# Calculate the area (in square meters) of each polygon in the GeoDataFrame
regions.loc[:, "AREA"] = regions.geometry.area / 10**6

print("Area of Ghana: {} square kilometers".format(regions.AREA.sum()))
print("CRS:", regions.crs)
print(regions.head())
