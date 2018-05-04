#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 11:40:36 2018

Rasterio cut shape from raster

@author: cake
"""
import rasterio
from rasterio.tools.mask import mask


"""
Corner Coordinates:
Upper Left  (  281085.000, 8920515.000) (  3d27'35.37"E, 80d 9'12.49"N)
Lower Left  (  281085.000, 8648685.000) (  5d42'54.05"E, 77d45'27.07"N)
Upper Right (  553215.000, 8920515.000) ( 17d50'27.43"E, 80d20'13.64"N)
Lower Right (  553215.000, 8648685.000) ( 17d16'31.42"E, 77d54'14.26"N)
Center      (  417150.000, 8784600.000) ( 11d 4'13.00"E, 79d 6'21.74"N)
"""

fn = r'../landsat/02-08-2017/LC08_L1TP_220003_20170802_20170812_01_T1_B10.TIF'

''' Shape'''
lat = 439246.000
lon = 8772767.000

minLon = lon - 1500
minLat = lat - 2500
maxLon = lon + 1500
maxLat = lat + 2500

geoms = [{'type': 'Polygon', 'coordinates': [[(minLat, minLon), 
                                              (maxLat, minLon),
                                              (maxLat, maxLon),
                                              (minLat, maxLon), 
                                              (minLat, minLon)]]}]

# load the raster, mask it by the polygon and crop it
with rasterio.open(fn) as src:
    out_image, out_transform = mask(src, geoms, crop=True)
out_meta = src.meta.copy()

# save the resulting raster  
out_meta.update({"driver": "GTiff",
    "height": out_image.shape[1],
    "width": out_image.shape[2],
"transform": out_transform})

with rasterio.open("masked.tif", "w", **out_meta) as dest:
    dest.write(out_image)

io.imshow('masked.tif')

#
#
##%%
#import fiona
#import rasterio
#import rasterio.mask
#
#with fiona.open(shape, "r") as shapefile:
#    features = [feature["geometry"] for feature in shapefile]
#    
#with rasterio.open(fn) as src:
#    out_image, out_transform = rasterio.mask.mask(src, features,
#                                                        crop=True)
#    out_meta = src.meta.copy()
#
#    