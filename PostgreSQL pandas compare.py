# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 21:29:50 2019

@author: Jim

The first part of this program joins two tables in a PostgreSQL database to
produce a short report.  The second part reads the same two tables into two
pandas dataframes, then uses pandas to join the dataframes and create a
report identical to the report created in the first part.

"""

import psycopg2
import pandas as pd
from sqlalchemy import create_engine


def get_query(query):
    db = psycopg2.connect(dbname='news',
                          user='postgres',
                          password='xxxxxxxx',
                          host='localhost',
                          port=5432)
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def top_articles():
    query = ("""
        select articles.title,
               views
        from articles,
             (select path,
                     count(*) as views
              from log
              group by path) as agglog
        where agglog.path = '/article/' || articles.slug
        order by views desc limit 3;""")
    results = get_query(query)
    print("\nWhat are the top three articles of all time?\n")
    for article, views in results:
        print("  {}  --  {} views".format(article, views))


top_articles()

engine = create_engine('postgresql://postgres:xxxxxxxx@localhost:5432/news')

dfarticles = pd.read_sql('select * from articles', engine)
dflog = pd.read_sql('select * from log', engine)

dfjoin = pd.merge(dfarticles,
                  dflog,
                  left_on='/article/' + dfarticles.slug,
                  right_on=dflog.path)

pp = dfjoin.title.value_counts().to_frame()
pp.reset_index(inplace=True)
pp.columns = ['title', 'views']

print('\nWhat are the top three articles of all time?\n')
for i in range(0, 3):
    print('  {}  --  {} views'.format(pp.iloc[i].title, pp.iloc[i].views))
