import geopandas as gpd


SA1 = gpd.read_file('abs_data/gis/sa1/sa1.shp').dropna(subset=['geometry'])
SA2 = gpd.read_file('abs_data/gis/sa2/sa2.shp').dropna(subset=['geometry'])