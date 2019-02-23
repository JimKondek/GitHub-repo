# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 20:06:46 2018

@author: Jim
"""

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:xxxxxxxx@localhost:5432/news')

query = """
    select date(time),
           sum(case when status = '200 OK' then 1 else 0 end) as good,
           sum(case when status != '200 OK' then 1 else 0 end) as bad
    from log
    group by date(time)
    order by date(time)
"""

df = pd.read_sql_query(query, con=engine)

plt.figure(figsize=(8, 6))

plt.ylim(25000, 60000)

plt.plot(df.date, df.good)
plt.plot(df.date, df.good + df.bad)
plt.savefig('July 2016.png')
