# -*- coding: utf-8 -*-
"""
Created on Sun May 16 13:34:52 2021

@author: Jim
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

# This file has about 903K rows as of May 2021.

url = "https://data.seattle.gov/api/views/tazs-3rd5/rows.csv"

df = pd.read_csv(url, low_memory=False)

# The Latitude and Longitude columns contain the property latitude and
# longitude to six decimal places.  The rounding precision affects the
# degree of granularity of the resulting heatmap.

precision = 3
df['Lat'] = df['Latitude'].round(precision)
df['Lon'] = df['Longitude'].round(precision)

df = df[df.Offense.str.contains('Motor Vehicle Theft', na=False)]
df["StartDate"] = pd.to_datetime(df["Offense Start DateTime"])

df = df[(df.StartDate > "2011-01-01") & (df.StartDate < "2020-01-01")]

# Get rid of data with zero longitude values.
da = df[df.Lon != 0]

# "City of Seattle Shoreline" available at the City of Seattle Open Data Portal
# https://data.seattle.gov/
# load seattle shape
cities = gpd.read_file(r'c:\users\jim\seapets\Municipal_Boundaries.shp')
seattle = cities.loc[cities['CITYNAME'] == 'Seattle']
seattle = seattle.reset_index()
seattle_shp = seattle.loc[0, 'geometry']

# load seattle waterfront shape
waterfront = gpd.read_file(r'c:\users\jim\seapets\City_of_Seattle_Shoreline.shp')

heatmap, xedges, yedges = np.histogram2d(da.Lon, da.Lat, bins=(150,200))
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.clf()
fig, ax = plt.subplots(figsize=(16,26))
plt.imshow(heatmap.T,
           extent=extent,
           origin='lower',
           vmax=40,
           cmap='gist_yarg')
waterfront.plot(ax=ax,
                color='blue',
                linewidth=0.5)
seattle.plot(ax=ax,
             color='none',
             edgecolor='black',
             linewidth=0.5,
             linestyle='dotted')
plt.show()
