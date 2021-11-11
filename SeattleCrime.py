# -*- coding: utf-8 -*-
"""
Created on Sun May 16 13:34:52 2021

@author: Jim
"""

import pandas as pd
import seaborn as sns
from datetime import datetime

print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# This file has about 903K rows as of May 2021.

url = "https://data.seattle.gov/api/views/tazs-3rd5/rows.csv"

df = pd.read_csv(url, low_memory=False)

print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# The Latitude and Longitude columns contain the property latitude and
# longitude to six decimal places.  The rounding precision affects the
# degree of granularity of the resulting heatmap.

precision = 3
df['Lat'] = df['Latitude'].round(precision)
df['Lon'] = df['Longitude'].round(precision)

df = df[df.Offense.str.contains('Motor Vehicle Theft', na=False)]
df["StartDate"] = pd.to_datetime(df["Offense Start DateTime"])

df = df[(df.StartDate > "2011-01-01") & (df.StartDate < "2020-01-01")]

df_all = pd.DataFrame(data=df.groupby(['Lat', 'Lon']).size(),
                      columns=['all_value'])
df_all.reset_index(inplace=True)

df_all['Lat'] = df_all['Lat'] * -1

result = df_all.pivot(index='Lat', columns='Lon', values='all_value')

# Flip the heatmap colorbar so that it's light to dark, then set the scale.
cmap = sns.cm.rocket_r
sns.set(rc={'figure.figsize': (8, 14)})

# Create the heatmap and save it if desired.  The vmin and vmax values
# represent the mininum and maximum values of the result.
hm = sns.heatmap(result, vmin=0.0, vmax=50.0, cmap=cmap)
print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
