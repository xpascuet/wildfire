# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 20:59:36 2022

@author: Xavi Pascuet
"""

import burned_area_utils
from sentinelhub import SHConfig


#  Import SentineHub configuration
config = SHConfig()

# Define fire area
bbox = [0.687224, 41.582167, 0.720308, 41.604870]

fire_start_day = "2022-06-10"
fire_end_day = "2022-06-10"

# Set sentinel bands
band1 = 4
band2 = 5
# Download tiffs
pre_folder, post_folder = burned_area_utils.get_tiffs(
    bbox, fire_start_day, fire_end_day)

# Extract prefire bands
prefire_b8A, _crs, geoTransform, tarjetprj = burned_area_utils.read_band_image(
    band1, pre_folder)
prefire_b12, _crs, geoTransform, tarjetprj = burned_area_utils.read_band_image(
    band2, pre_folder)

# Calculate of pre-fire NBR
prefire_nbr = burned_area_utils.nbr(
    prefire_b8A.astype(int), prefire_b12.astype(int))

# Extract postfire bands
postfire_b8A, _crs, geoTranform, tarjetprj = burned_area_utils.read_band_image(
    band1, post_folder)
postfire_b12, _crs, geoTranform, tarjetprj = burned_area_utils.read_band_image(
    band2, post_folder)

# Calculate pre-fire NBR
postfire_nbr = burned_area_utils.nbr(
    postfire_b8A.astype(int), postfire_b12.astype(int))

# Calculate NBR diference
dNBR = burned_area_utils.dnbr(prefire_nbr, postfire_nbr)

# Export result
burned_area_utils.array2raster(dNBR, geoTransform, _crs, "dNBR.tiff")

# Transform to polygon
burned_area_utils.poligonize("dNBR.tiff", "area_cremada2.geojson")
