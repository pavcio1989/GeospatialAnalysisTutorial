import pandas as pd
import geopandas as gpd
import numpy as np
import folium
from folium import Marker
from geopy.geocoders import Nominatim
import warnings
warnings.filterwarnings('ignore')


geolocator = Nominatim(user_agent="kaggle_learn")
location = geolocator.geocode("Pyramid of Khufu")

print(location.point)
print(location.address)

point = location.point
print("Latitude:", point.latitude)
print("Longitude:", point.longitude)

universities = pd.read_csv("./data/inputs/04/top_universities.csv")
universities.head()


def my_geocoder(row):
    try:
        _point = geolocator.geocode(row).point
        return pd.Series({'Latitude': _point.latitude, 'Longitude': _point.longitude})
    except:
        return None


universities[['Latitude', 'Longitude']] = universities.apply(lambda x: my_geocoder(x['Name']), axis=1)

print("{}% of addresses were geocoded!".format(
    (1 - sum(np.isnan(universities["Latitude"])) / len(universities)) * 100))

# Drop universities that were not successfully geocoded
universities = universities.loc[~np.isnan(universities["Latitude"])]
universities = gpd.GeoDataFrame(
    universities, geometry=gpd.points_from_xy(universities.Longitude, universities.Latitude))
universities.crs = {'init': 'epsg:4326'}
print(universities.head())

# Create a map
m = folium.Map(location=[54, 15], tiles='openstreetmap', zoom_start=2)

# Add points to the map
for idx, row in universities.iterrows():
    Marker([row['Latitude'], row['Longitude']], popup=row['Name']).add_to(m)

# Display the map
m.save("./data/outputs/04/geocoded_locations.html")

# Attribute joins
pd.set_option('display.max_columns', None)

world = gpd.read_file("data/inputs/04/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")
print(f"World DF:")
print(world.head())

europe = world.loc[world.CONTINENT == 'Europe'].reset_index(drop=True)

europe_stats = europe[["NAME_EN", "POP_EST", "GDP_MD"]].rename(columns={"NAME_EN": "name"})
europe_boundaries = europe[["NAME_EN", "geometry"]].rename(columns={"NAME_EN": "name"})

# Use an attribute join to merge data about countries in Europe
europe = europe_boundaries.merge(europe_stats, on="name")
print("Europe dataframe:\n")
print(europe.head())

# Use spatial join to match universities to countries in Europe
european_universities = gpd.sjoin(universities, europe)

# Investigate the result
print("We located {} universities.".format(len(universities)))
print("Only {} of the universities were located in Europe (in {} different countries).".format(
    len(european_universities), len(european_universities.name.unique())))

print(european_universities.head())
