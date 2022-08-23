# Sqlalchemy-Challenge


## Background:  
SQLAlchemy is a toolkit of Python SQL that provides us with flexibility of using SQL databse. It considers the database to be a relational algebra engine, not just a collection of tables. We can select rows not only from tables but through joins and other select statments. SQLAlchemy is most famous for its object-relational mapper (ORM) which is a technique used to convert data between databases or OOP languages (Java, Python and C++.) such as Python.


## Configuration: 

In this assignment, we need to do some climate analysis of our vacation destination. The destination is Honolulu, Hawaii. We need to do the following inorder to complete our task


### Part 1: Climate Analysis and Exploration

In this section, we need to use Python and SQLAlchemy to perform basic climate analysis and data exploration of the climate database given.

* We need to use the provided [starter notebook](climate_starter.ipynb) and [hawaii.sqlite](Resources/hawaii.sqlite) files to complete our climate analysis and data exploration.

* We would use SQLAlchemy’s `create_engine` to connect to our SQLite database.

* We would use SQLAlchemy’s `automap_base()` to reflect our tables into classes and save a reference to those classes called `Station` and `Measurement`.

* We need to link Python to the database by creating a SQLAlchemy session.

* And lastly, we need to close out our session at the end of our notebook.

#### Precipitation Analysis

To perform an analysis of precipitation in the area, we need to do the following:

* Find the most recent date in the dataset.

* Using this date, retrieve the previous 12 months of precipitation data by querying the 12 previous months of data. 

* Select only the `date` and `prcp` values.

* Load the query results into a Pandas DataFrame, and set the index to the date column.

* Sort the DataFrame values by `date`.

* Plot the results by using the DataFrame `plot` method.

* Use Pandas to print the summary statistics for the precipitation data.

#### Station Analysis

To perform an analysis of stations in the area, we need to do the following:

* Design a query to calculate the total number of stations in the dataset.

* Design a query to find the most active stations (the stations with the most rows).

    * List the stations and observation counts in descending order.

    * Which station id has the highest number of observations?

    * Using the most active station id, calculate the lowest, highest, and average temperatures.

    * We will need to use functions such as `func.min`, `func.max`, `func.avg`, and `func.count` in our queries.

* Design a query to retrieve the previous 12 months of temperature observation data (TOBS).

    * Filter by the station with the highest number of observations.

    * Query the previous 12 months of temperature observation data for this station.

    * Plot the results as a histogram with `bins=12`.

    * Close out our session.

### Part 2: Design Your Climate App

For this part, we need to design a Flask API based on the queries that we developed above.

We will use Flask to create our routes, as follows:

* `/`

    * Homepage.

    * List all available routes.

* `/api/v1.0/precipitation`

    * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

    * Return the JSON representation of our dictionary.

* `/api/v1.0/stations`

    * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`

    * Query the dates and temperature observations of the most active station for the previous year of data.

    * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

    * Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.

    * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than or equal to the start date.

    * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates from the start date through the end date (inclusive).


### Conclusion :

From the tables and graphs, the temperatures for honululu, hawaii ranges mostly between 70-80 degrees farenheit. This is a good weather for us to enjoy our holiday trip. 
![Image](images/histogram_of_tempObs.png)
From the precipitation plot, we can see that the best time of year to go for our trip would be in August. As the precipitation values are less in August
![Image](images/line-plot-of-precipitation.png) 