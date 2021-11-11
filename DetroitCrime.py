# -*- coding: utf-8 -*-
"""
Created on Wed May 19 10:07:59 2021

@author: Jim
"""

import pandas as pd
import seaborn as sns

url = "https://opendata.arcgis.com/datasets/0825badfe6304620a998d162be0e135e_0.csv"

df = pd.read_csv(url, low_memory=False)

# The Latitude and Longitude columns contain the property latitude and
# longitude to six decimal places.  The rounding precision affects the
# degree of granularity of the resulting heatmap.
precision = 3
df['Lat'] = df['latitude'].round(precision)
df['Lon'] = df['longitude'].round(precision)

df_all = pd.DataFrame(data=df.groupby(['Lat', 'Lon']).size(),
                      columns=['all_value'])
df_all.reset_index(inplace=True)

df_all['Lat'] = df_all['Lat'] * -1

result = df_all.pivot(index='Lat', columns='Lon', values='all_value')

# Flip the heatmap colorbar so that it's light to dark, then set the scale.
cmap = sns.cm.rocket_r
sns.set(rc={'figure.figsize': (14, 8)})

# Create the heatmap and save it if desired.  The vmin and vmax values
# represent the mininum and maximum values of the result.
hm = sns.heatmap(result, vmin=0.0, vmax=50.0, cmap=cmap)
