# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 16:53:50 2019

@author: Jim

Reads a CSV file obtained from the City of Detroit's Open Data Portal.  This
file contains information regarding blight tickets.  I wrote this program to
create a Seaborn heatmap showing the number of paid-in-full blight tickets
within a set of grids defined by latitude and longitude.  The resulting
heatmap thus resembles a map of the city of Detroit.

"""

import pandas as pd
import seaborn as sns

url = "https://opendata.arcgis.com/datasets/fe2f692918a04c13a6cead436e7eaec9_0.csv"

df = pd.read_csv(url, low_memory=False)

# The X and Y columns contain the property latitude and longitude to six
# decimal places.  The rounding precision affects the degree of granularity
# of the resulting heatmap.
precision = 3
df['Lat'] = df['X'].round(precision)
df['Lon'] = df['Y'].round(precision)

# df1 represents all violations (the disposition column will contain the
# string 'Responsible' in its value). df2 represents all paid in full
# violations (the balance_due column value is zero).
df1 = df[df.disposition.str.contains('Responsible', na=False)]
df2 = df1[df1['balance_due'] == 0]

df_all = pd.DataFrame(data=df1.groupby(['Lat', 'Lon']).size(),
                      columns=['all_value'])
df_good = pd.DataFrame(data=df2.groupby(['Lat', 'Lon']).size(),
                       columns=['good_value'])
df_all.reset_index(inplace=True)
df_good.reset_index(inplace=True)

# One way to get the heatmap to print rightside up is to negate the
# latitude and longitude.
df_all['Lon'] = df_all['Lon'] * -1
df_good['Lon'] = df_good['Lon'] * -1

# We join the df_all and df_good dataframes to compute the percentage of
# all paid-in-full tickets within each latitude/longitude aggregation.
# A pivot table of the results will be used to create the heatmap.
dftest = df_all.merge(df_good, how='left', on=['Lat', 'Lon'])
dftest['compute'] = dftest['good_value'] / dftest['all_value']
result = dftest.pivot(index='Lon', columns='Lat', values='compute')

# Flip the heatmap colorbar so that it's light to dark, then set the scale.
cmap = sns.cm.rocket_r
sns.set(rc={'figure.figsize': (28, 16)})

# Create the heatmap and save it if desired.  The vmin and vmax values
# represent the mininum and maximum values of the paid-in-full percentage.
hm = sns.heatmap(result, vmin=0.0, vmax=1.0, cmap=cmap)
# fig = hm.get_figure()
# fig.savefig("DetoutHM.png")
