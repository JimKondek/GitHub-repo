### GitHub-repo

This repository contains some simple examples of code and output that I've recently created, also several analyses.  All of these files are original work.  This README file describes each of the other files in the repository.

**bubblesorttest.py, Bubble sort output** - As part of a technical job interview, the candidate is sometimes asked to write sample code to accomplish a common task.  This demonstrates that the candidate has some competency in the language used to write the sample code.  These two files represent my attempt to write a Python program that uses two slightly different techniques to "bubble sort" a Python list of ten thousand random numbers.  One technique skips list entries that have already been sorted.  Both techniques are timed and the results printed at the end of the program.  Both results are shown to be the same; the second technique is shown to be faster than the first.

**DetroitBlight.py, DetoutHM.png** - For the final project in my Coursera machine learning class, I was tasked with creating a classifier (using the Python scikit-learn library) that could predict whether blight violation tickets written by the city of Detroit would be paid or not.  The project grade depended on the value of the resulting "area under the curve" (AUC) based on data provided by the city.  I have not included any actual classifier code in this repository because I don't want the code plagiarized.  However, I am including this Python program I wrote that used the seaborn library to create a "heat map" to determine whether more blight tickets were written in certain areas of the city than in others.  (The input comes from a file I had downloaded to my computer.)  I wasn't able to overlay an actual map of Detroit on the results, but I am very familiar with the city (I was born in Detroit) and could easily identify which areas and streets had more blight violations.  I did not submit this code as part of the project, but the resulting heat map gave me valuable perspective.

**DetroitCrime.py, SeattleCrime.py, TacomaCrime.py** - These three programs are influenced by the DetroitBlight.py program described above.  I accessed crime data from the public data portals of the cities of Detroit, Seattle and Tacoma.  Based on the location of where a crime was committed, I created heat maps showing the frequency of crimes in each area of the city.  As with the DetroitBlight.py program, I haven't overlaid an actual map, but to anyone familiar with these cities, these heat maps will strongly resemble actual maps.  The input columns are slightly different from city to city.

**LatestBlight.py, LatestHM.png** - Very similar to DetroitBlight.py and DetoutHM.png.  The Python code uses the pandas read_csv routine to download a file of blight ticket information directly from the City of Detroit's Open Data Portal.  The code computes the percentage of paid blight tickets vs. all tickets within each grid area, then creates a heat map of the results.  The idea behind this heat map is to see if there are certain areas in the city where blight tickets are more likely to be paid in full.  Modifying the grid size (by varying the precision used to round the latitude and longitude of each property) gave me some insights.

**obj_sort.txt, obj_nosort.txt** - These two files make up a two-part analysis I wrote that discusses the conditions under which the Oracle optimizer will choose to use an index when executing a query containing a "range" test (i.e. when a column contains a value that falls between two specified values) within the WHERE clause.  This is an example of the kind of work I did when attempting to tune underperforming queries.  (There is some simple Markdown formatting in these files to help delineate the actual SQL statements I used, so it may be better to open these files using a Markdown viewer.)

**Oracle external table preprocessing.txt** - This analysis describes how I was able to use Oracle's external table preprocessing feature to directly access an online CSV file using a Python program, without any need for intermediate files.  Though the DBA needs to do a little setup, the user need only run a simple SELECT statement.

**PostgreSQL pandas compare.py, PostgreSQL pandas compare output** - These two files provide a simple comparison between using a SELECT statement to join two database tables versus using the pandas library to build and join two pandas dataframes from the same two tables.  The output file shows the (identical) results of the two techniques.  I did not compare the elapsed times of both techniques; the pandas technique takes longer because the dataframes need to be built every time the program is run, and one of the dataframes contains about 1.7 million rows.  (The PostgreSQL database used here is from one of the Udacity projects I reviewed.)

**PostgreSQL engine example.py, July 2016.png** - This simple Python program first uses the sqlalchemy library instead of the psycopg2 library to connect to a PostgreSQL database.  It then creates a pandas dataframe using the read_sql_query routine.  Finally it plots a very simple matplotlib graph of the dataframe.  The second file contains sample output.  (The plot lines drop on the far right of the graph because the table contains only partial data for the last day of July.)

**SeattleCrime.png** - This is the heat map produced by the version of SeattleCrime.py that I've uploaded.  It records the number of motor vehicle thefts reported between 2011 and 2019.  Those familiar with Seattle neighborhoods will note that many thefts are concentrated in downtown, Capitol Hill and the University District.

**Week 2 Assignment** - This graph was the deliverable for the second weekly assignment in my "Applied Plotting, Charting and Data Representation in Python" course.  The assignment was to create a graph that would display the highest and lowest termperatures by day between 2005 and 2014 near Seattle, Washington, along with days in 2015 where the maximum or minimum were exceeded.  To create this graph I wrote Python code to call the matplotlib library using a Jupyter Notebook.
