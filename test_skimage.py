#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 00:13:50 2018

@author: esw3@aber.ac.uk
"""
import skimage.io as io
import pandas as pd
import numpy as np


from shapely import geometry
import osgeo.ogr as ogr
import geopandas as gpd


#import subprocess
import rasterio

##%%
#''' Shape'''
#lat = 79.01145
#lon = 12.13234
#
#minLong = lon - 5
#minLat =  lat - 5
#maxLong = lon + 5
#maxLat = lat + 5
#
##polygon = geometry.Polygon([[0, 0], 
##                   [1, 0], 
##                   [1, 1], 
##                   [0, 1]])
#
#linearRing = ogr.Geometry(ogr.wkbLinearRing)
#linearRing.AddPoint(minLong, minLat)
#linearRing.AddPoint(maxLong, minLat)
#linearRing.AddPoint(maxLong, maxLat)
#linearRing.AddPoint(minLong, maxLat)
#linearRing.AddPoint(minLong, minLat)
#
#polygon = ogr.Geometry(ogr.wkbPolygon)
#polygon.AddGeometry(linearRing)
#

#%%
'''conversion constants for band 10 and 11''' 	
#Radiance Multiplier
rm_10 = 0.0003342	
rm_11 = 0.0003342

#Radiance Add
ra_10 = 0.1
ra_11 = 0.1

#K1
k1_10 = 774.89
k1_11 = 480.89

#K2
k2_10 = 1321.08
k2_11 = 1201.14

'''
Stage 1: a) Open the image
         b) Convert raw to TOA
         c) Convert TOA to Kelvin -> Celsius
'''
fn = r'masked.tif'
lsim = io.imread(fn, plugin='tifffile')

def convertTOA(file, rmult, ra):
    '''
    convert digital number to at sensor/top of atmosphere radiance
    y = mx + b --> y = rm * file + ra
    '''
    toa = (rmult * file) + ra
    return(toa)

def convertTemp(toa, k1, k2):
    '''
    Convert toa to temperature in Kelvin
    '''
    kelvins = k2 / ( (k1/toa) +1 )
    return(kelvins)
    
x = convertTOA(lsim, rm_10, ra_10)
y = convertTemp(x, k1_10, k2_10)

'''
Stage 2: Cut the polygon from the image which we want to work with

'''
##%% 
##import rasterio
#from rasterio.mask import mask
##import geopandas as gpd
#
#shape = r'./wrs2/wrs2_descending.shp'
#shapefile = gpd.read_file(shape)
#
## extract the geometry in GeoJSON format
#geoms = shapefile.geometry.values # list of shapely geometries
#geometres = geoms[0] # shapely geometry
#
#
## transform to GeJSON format
#from shapely.geometry import mapping
#geoms = [mapping(geoms[0])]
#
## extract the raster values values within the polygon 
#with rasterio.open(fn) as src:
#     out_image, out_transform = mask(src, geoms, crop=True)
#

#%%
'''
Stage 3: a) Create a mask for that subset which contains min/max values for display
         b) Read this as a shapefile if necessary
'''
min_value = y.min()
max_value = y.min() + 5
mask = (min_value < y) & (y < max_value)



'''
Stage 4: Calculate the area covered by pixels inside mask

'''


'''
Stage 5: Can we animate this over image(s) to check if true?

'''
    