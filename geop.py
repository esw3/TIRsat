# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 19:16:52 2018

@author: cake
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import pyproj
import folium
from shapely import geometry
import matplotlib.pyplot as plt

#import pandas as pd
#import geopandas as gpd
#import folium
import os, shutil
from glob import glob
import shapefile


WRS_PATH = './wrs2_descending.zip'
LANDSAT_PATH = os.path.dirname(WRS_PATH)
#!wget -P {LANDSAT_PATH} https://landsat.usgs.gov/sites/default/files/documents/wrs2_descending.zip

shutil.unpack_archive(WRS_PATH, os.path.join(LANDSAT_PATH, 'wrs2'))
wrs = gpd.GeoDataFrame.from_file('./wrs2/wrs2_descending.shp')

#wrs.head()

#sf = shapefile.Reader("/home/cake/2018/tir/python/test.shp")
sf2 = gpd.GeoDataFrame.from_file('/home/cake/2018/tir/python/test.shp')
#sf2.crs = {'init' : 'epsg:3857'}

wrs_intersection = wrs[wrs.intersects(sf2.geometry[0])]

paths, rows = wrs_intersection['PATH'].values, wrs_intersection['ROW'].values

#m = folium.Map(location=center, zoom_start=zoom, control_scale=True)
#map=folium.Map(location=[df['LAT'].mean(),df['LON'].mean()],zoom_start=6,tiles='Mapbox bright')

#npolar:
#UTM33X: E439002, N8772750
#UTM35X: E186917, N8811369
#DD.DDDDD: 79.01145°N, 12.13234°E
#DDMM.MMM: 79°00.687'N, 12°07.941'E
#DDMMSS.S: 79°00'41.2"N, 12°07'56.4"E

lat = 79.01145
lon = 12.13234
zoom=6
m = folium.Map(location=[lat,lon], zoom_start=zoom, control_scale=True)

m.add_child(folium.GeoJson(sf2, name='Area of Study', 
                           style_function=lambda x: {'color': 'red', 'alpha': 0}))

# Iterate through each Polygon of paths and rows intersecting the area
for i, row in wrs_intersection.iterrows():
    # Create a string for the name containing the path and row of this Polygon
    name = 'path: %03d, row: %03d' % (row.PATH, row.ROW)
    # Create the folium geometry of this Polygon 
    g = folium.GeoJson(row.geometry.__geo_interface__, name=name)
    # Add a folium Popup object with the name string
    g.add_child(folium.Popup(name))
    # Add the object to the map
    g.add_to(m)

folium.LayerControl().add_to(m)
m.save('./wrs.html')
m


#b = (paths > 23) & (paths < 26)
#paths = paths[b]
#rows = rows[b]

for i, (path, row) in enumerate(zip(paths, rows)):
    print('Image', i+1, ' - path:', path, 'row:', row)
    
# Empty list to add the images
bulk_list = []

s3_scenes = pd.read_csv('http://landsat-pds.s3.amazonaws.com/c1/L8/scene_list.gz', compression='gzip')
# Iterate through paths and rows

#for path, row in zip(paths, rows):

for i, (path, row) in enumerate(zip(paths, rows)):
    print('Path:',path, 'Row:', row)

    # Filter the Landsat Amazon S3 table for images matching path, row, cloudcover and processing state.
    scenes = s3_scenes[(s3_scenes.path == path) & (s3_scenes.row == row) & 
                       (s3_scenes.cloudCover <= 5) & 
                       (~s3_scenes.productId.str.contains('_T2')) &
                       (~s3_scenes.productId.str.contains('_RT'))]

    print(' Found {} images\n'.format(len(scenes)))

    # If any scenes exists, select the one that have the minimum cloudCover.
    if len(scenes):
        scene = scenes.sort_values('cloudCover').iloc[0]
        # Add the selected scene to the bulk download list.
        bulk_list.append(scene)
    