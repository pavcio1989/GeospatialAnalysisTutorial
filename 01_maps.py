import geopandas as gpd
import matplotlib.pyplot as plt


# Read in the data
full_data = gpd.read_file("data/inputs/01/DEC_lands/DEC_lands.shp")

data = full_data.loc[:, ["CLASS", "COUNTY", "geometry"]].copy()

# How many lands of each type are there?
print(data.CLASS.value_counts())

# Select lands that fall under the "WILD FOREST" or "WILDERNESS" category
wild_lands = data.loc[data.CLASS.isin(['WILD FOREST', 'WILDERNESS'])].copy()

wild_lands.plot()
plt.show()

# Campsites in New York state (Point)
POI_data = gpd.read_file("data/inputs/01/DEC_pointsinterest/Decptsofinterest.shp")
campsites = POI_data.loc[POI_data.ASSET=='PRIMITIVE CAMPSITE'].copy()

# Foot trails in New York state (LineString)
roads_trails = gpd.read_file("data/inputs/01/DEC_roadstrails/DEC_roadstrails/Decroadstrails.shp")
trails = roads_trails.loc[roads_trails.ASSET=='FOOT TRAIL'].copy()

# County boundaries in New York state (Polygon)
counties = gpd.read_file("data/inputs/01/NY_county_boundaries/NY_county_boundaries/NY_county_boundaries.shp")

# Define a base map with county boundaries
ax = counties.plot(figsize=(10,10), color='none', edgecolor='gainsboro', zorder=3)

# Add wild lands, campsites, and foot trails to the base map
wild_lands.plot(color='lightgreen', ax=ax)
campsites.plot(color='maroon', markersize=2, ax=ax)
trails.plot(color='black', markersize=1, ax=ax)
plt.show()
