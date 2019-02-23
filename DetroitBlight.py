# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 21:29:50 2019

@author: Jim

Reads a CSV file obtained from the City of Detroit website.  This file
contains information regarding blight tickets.  I used this code to create
a heatmap showing the number of tickets written in a set of grids
defined by latitude and longitude.  The resulting Seaborn heat map thus
resembles a map of the city of Detroit.

"""

import pandas as pd
import seaborn as sns

df = pd.read_csv("c:/users/jim/downloads/Blight_Violations.csv",
                 low_memory=False)

df['Lat'] = df['Violation Latitude'].round(4)
df['Lon'] = df['Violation Longitude'].round(4)

# dflatlon = df.groupby(['Lat', 'Lon']).size()
dfxy = pd.DataFrame(data=df.groupby(['Lat', 'Lon']).size(), columns=['value'])
dfxy.reset_index(inplace=True)
dfxy['Lat'] = dfxy['Lat'] * -1

result = dfxy.pivot(index='Lat', columns='Lon', values='value')

# Flip the heatmap colorbar so that it's light to dark.
cmap = sns.cm.rocket_r

sns.set(rc={'figure.figsize': (28, 16)})
sns.heatmap(result, vmin=0, vmax=20, cmap=cmap)

hm = sns.heatmap(result, vmin=0, vmax=20, cmap=cmap)
fig = hm.get_figure()
fig.savefig("DetoutHM.png")
