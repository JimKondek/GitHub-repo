# -*- coding: utf-8 -*-
"""
Created on Tue May 18 09:17:44 2021

@author: Jim
"""

import pandas as pd
import seaborn as sns
from ast import literal_eval

# The crime dataset from the city of Tacoma contains these columns:
# Incident Number, Crime, Occurred On, Approximate Time, Intersection
# The latitude and longitude is embedded in the Intersection column
# and requires extraction (see below)

# The input file is about 122K rows as of May 2021.

url = "https://data.cityoftacoma.org/api/views/mtzj-ngek/rows.csv"

df = pd.read_csv(url, low_memory=False)

# Extract the latitude and longitude from within the "intersection" column.

df["tuplit"] = df.intersection.str.split(pat='\n', expand=True)[2]

# Get rid of nan entries, otherwise literal_eval will throw an error.

df = df.dropna()
df[["Latitude", "Longitude"]] = [(literal_eval(x)[0], literal_eval(x)[1])
                                 for x in df.tuplit]

# The Latitude and Longitude columns contain the property latitude and
# longitude to six decimal places.  The rounding precision affects the
# degree of granularity of the resulting heatmap.

precision = 3
df['Lat'] = df['Latitude'].round(precision)
df['Lon'] = df['Longitude'].round(precision)

# df1 = df[df.Crime.str.contains('Motor Vehicle Theft', na=False)].dropna()
# df1["StartDate"] = pd.to_datetime(df1["Offense Start DateTime"])

df_all = pd.DataFrame(data=df.groupby(['Lat', 'Lon']).size(),
                      columns=['all_value'])
df_all.reset_index(inplace=True)

# The file contains a fair amount of latitude values far from Tacoma.
# Let's reject those rows and zero in on the Tacoma area.

df_all = df_all[(df_all.Lat > 47.0) & (df_all.Lat < 48.0)]

# To get the heatmap rightside up, we negate the latitude values,
# then create a pivot table using the latitude values for the index,
# the longitude values as the column names, and the accumulations
# by latitude|longitude from df_all.all_value.

df_all['Lat'] = df_all['Lat'] * -1
result = df_all.pivot(index='Lat', columns='Lon', values='all_value')

# Flip the heatmap colorbar so that it's light to dark, then set the scale.
cmap = sns.cm.rocket_r
sns.set(rc={'figure.figsize': (14, 10)})

# Create the heatmap and save it if desired.  The vmin and vmax values
# represent the mininum and maximum values of the result.
hm = sns.heatmap(result, vmin=0.0, vmax=200.0, cmap=cmap)
