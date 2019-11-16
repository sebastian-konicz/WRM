# Wroclaw Bikesharing System Analysis
==============================

## Overview
As part of the free transport data service, Wroclaw Bikesharing System (WRM) release data on journeys taken using their cycles. The data goes back to June 2019, showing information on the start and end locations of the journey along with time of day. By combining this information with the coordinates of each cycle hire point, I predicted the most likely journey taken for each start/end combination.

## Table of contents
1. [Basic Statistics](#statistics)
2. [Usage patterns](#usage_patterns)
3. [Weather conditions usage patterns](#weather)
4. [Bike Stations Analysis](#stations)
5. [Route predictions](#route)

## Basic Statistics
<a id="statistics"></a>
- number of bikes
- number of docking stations
- total number of rentals
- total number of valid rentals (>5 minutes and not between the same station)
- most popular docking station / least popular docking station
- most popular bike  / least popular bike
- most popular paths / least popular paths
- average rental time
- record day
- record month

## Usage patterns
<a id="usage_patterns"></a>
(How does usage change across the year, the week, and the day?)
- Average(by day)/Total count by month
- Average(by hour)/Total count by day
- Average/Total count by hour of the day
- Average count by hour of the day (accrow weekdays)
	(Are people mostly using Bike Share as a way to commute to work or to explore the city?)
	- inflow / outflow pictures (with color codes)
- Count by hour of the day (workdays, weekends and holidays)

- Histogram of rental time (comparison between workdays and weekends).

![monthAggPlot](images/plots/monthAggPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb)
![monthAvgPlot](images/plots/monthAvgPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb)
![dayAggPlot](images/plots/dayAggPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb)
![hourAggPlot](images/plots/hourAggPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb)
![hourAvgPlot](images/plots/hourAvgPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb)
![hourAvgWDPlot](images/plots/hourAvgWDPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb)
![hourAvgMonthPlot](images/plots/hourAvgMonthPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb)

[Source / Inspiration](https://medium.com/analytics-vidhya/how-to-finish-top-10-percentile-in-bike-sharing-demand-competition-in-kaggle-part-1-c816ea9c51e1)

## Weather conditions usage patterns
<a id="weather"></a>
(How does the weather change the way people use Bike Share?)
- correlation between weather conditions and bike usage (temp, percipity,

[Source / Inspiration](https://towardsdatascience.com/exploring-toronto-bike-share-ridership-using-python-3dc87d35cb62)

## Bike Stations Analysis
<a id="stations"></a>
- analysis of flows
	- vega map with count of rented bikes by hour
	- inflow and outflow gifs
- page rank algorithm
- redistribution mismatch (outflow - inflow)
- network analysis
	- bike paths graph

![All docking stations](images/final/DockingStationsMapBlack.png)
I've also generated a fancy interactive version of this plot in folium - click [here](https://sebastian-konicz.github.io/WRM/images/DockingStationsMapBlack.html) to see it. You can zoom/scroll with this version, and it also tells you the name and capacity of each location.

![Animation](images/final/IntensityMorning.gif)

[Source / Inspiration](https://github.com/charlie1347/TfL_bikes)

## Route predictions
<a id="route"></a>
- route prediction graph

[Source / Inspiration](https://github.com/charlie1347/TfL_bikes)


# The WRM data

Wroclaw host all of the raw cycle data on their [open data website](https://www.wroclaw.pl/open-data/dataset/wrmprzejazdy_data) as a series of CSV files. Furthermore, they also have [data](https://www.wroclaw.pl/open-data/dataset/nextbikesoap_data) showing the status of each bike point in Wroclaw, yielding information such as its coordinates, total capacity etc.

For those unaware, below is a map of all the cycle hire stations across Wroclaw and surrounding areas.






Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
