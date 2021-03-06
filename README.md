# Wroclaw Bikesharing System Analysis
==============================

## Overview
As part of the free transport data service, Wroclaw Bikesharing System (WRM) releases data on journeys taken using their cycles. The data goes back to April 2015, showing information on the start and end locations of the journey along with the time of day. By combining this information with the coordinates of each cycle hire point, I analyzed rental patterns among users (i.a. most popular destinations and paths), the popularity of certain docking stations and the correlation of rentals with weather conditions.

## Table of contents
1. [WRM Dataset overview](#dataset)
2. [Basic statistics](#statistics)
3. [Rental patterns](#rental_patterns)
4. [Bike stations analysis](#stations)
5. [Weather conditions usage patterns](#weather)
6. [Route predictions](#route)
7. [Conclusions](#conclusions")
8. [Project organisation](#project)

## WRM datasets overview <a id="dataset"></a>
Wroclaw host all of the raw cycle data on their [open data website](https://www.wroclaw.pl/open-data/dataset). There are two types of data available on the site:
1. [Actual data for bike rentals in 2019](https://www.wroclaw.pl/open-data/dataset/wrmprzejazdy_data/resource_history/65b5015e-070e-41da-8852-802a86442ac5)
2. [Historical data for years 2015 - 2016](https://www.wroclaw.pl/open-data/dataset/przejazdy-wroclawskiego-roweru-miejskiego-archiwalne)

Furthermore, they also have [data](https://www.wroclaw.pl/open-data/dataset/nextbikesoap_data) showing the status of each bike point in Wroclaw, yielding information such as its coordinates, total capacity, etc.

I've looked at both sets of data (actual and historical). The first dataset can be easily scraped from the internet (it is a series of CSV files), nevertheless a cursory review of the data reveals gaps in their continuity, e.g. there are separate files for periods from 2019-06-26 to 2019-07-14 but all those files have rental data only for 2019-06-26. Therefore, huge gaps in the continuity of data prevent proper analysis of rental trends.

The second set of data seems to be more consistent in terms of continuity, but the 2016 dataset has one crucial error i.e. from the first period to the end of October 2016 the starting station is the same as the end station.

Given the above, my analysis will concentrate only on the 2015 dataset with a total number of rows equal to 843 951.

### 2015 dataset
At first glance, the 2015 dataset is complete and consistent (no NaN values or missing data). Nevertheless, after a closer look, there are few issues concerning 2015 data.

#### Rental data vs docking stations data
The first issue with the 2015 dataset is connected with docking stations data i.e. the names of docking stations in the rental dataset do not match the names in docking stations dataset. Given the above, before merging two datasets, I had to manually add a new column in the docking station dataset and match the old names with the new ones. As a result of the above, I have discovered that 3 docking stations were present in 2015 but are not present today. These are:
1. Wyszyńskiego - Prusa
2. Teatralna - Piotra Skargi
3. Plac Nowy Targ

I have added them to the docking station dataset, gave them arbitrary ids and set respective GPS coordinates using google maps.
Furthermore, I have discovered that 8 docking stations were present in 2015 (but are not present today) and had only 1 or 2 rides. These are: Dworzec Głowny PKP, Grunwaldzka / Grochowska, Most Teatralny, Ogrody, Pętla Autobusowa - Dambonia, Plac Wolnosci, Poznań Główny, Wiejska / Pogodna.
The above stations were excluded from the dataset thus reducing the number of records from 843 951 to 843 937 (difference = 14).

#### Valid rentals based on location and duration
As a user of a similar bike-sharing system in my hometown (Warsaw), I know that often (especially when there are few bikes in the docking station) rented bikes do not work properly. Usually, the user can spot defected bikes right away (flat tire), but many times bike defects are apparent only after a brief ride.
As a result, some portion of bike rentals is "invalid" i.e. user returns the bike to the docking station after discovering the defect. Having that in mind, I have dropped from the dataset the rides that were made between the same docking station and shorter than 5 minutes. Obviously, the time value is arbitrary and can be changed in other analyzes, but in my opinion, it is hard to believe that many users rent a bike for such a small amount of time only to return it in the same docking station.
Given the above constraints, the dataset was reduced from 843 937 to 735 444 records (difference = 108 493).

Note: As the estimated number of invalid rentals is significant (12,8% of initial records) this issue will be the subject of a separate analysis in one of the chapters in the future.

#### Daylight saving time and negative duration
Due to change from summer time to winter time on 25 October 2015 i.e. retarding clocks by one hour at 3:00 am, some of the bike rentals had negative values. Obviously, these values had to be removed from the dataset for further analysis, hence reducing the number of records form 735 444 to 735 439 (difference = 5).

#### Speed
Usually, the bike-sharing system uses heavy and robust bikes that are not susceptible to mechanical failure and therefore they do not reach dizzying speeds. As an avid road cycling enthusiast with fairly good physical form, I know that it is very hard to accelerate such bike to a speed exceeding 25 km/h ipso facto I have limited the dataset to rides which on average do not exceed 25 km/h.
This procedure not only eliminates obvious errors in the bike-sharing system but also excludes rides that could have been done using other means of public transport (transporting a bicycle by bus or tram).
As a result, the dataset has been reduced from 735 439 to 733 429 (difference = 2 010).

## Basic statistics <a id="statistics"></a>
Based on the cleaned-up dataset I have prepared a table with basic statistics concerning the bike-sharing system in Wroclaw.
Readers can confront the data presented below with the official statistics available (in Polish) on this [site](https://www.wroclaw.pl/wroclawski-rower-miejski-podsumowanie-sezonu-2015).
Of course, the numbers differ, mainly because the bike-sharing operator overstates its statistics (probably for marketing purposes) by including all rentals (even the invalid ones).

![statisticsTable](images/plots/statisticsTable.png)

## Rental patterns <a id="rental_patterns"></a>
In this chapter, I will analyze the rental patterns of users to answer such questions as:
- how do usage change across the year, the week, and the day;
- are people mostly using the bike-sharing system as a way to commute to work or to explore the city;
- how long are the rides (short as a way to commute, or long as a form of recreation).

The following analysis was performed using charts prepared in plotly python library. Under each image, there is a link to an interactive version of the chart.

### Total and average bike rides by month
First of all, the subject of the analysis is the total number of bicycle rentals per month and its average value.

As you can see in the charts below, the most popular months (both in terms of total and average loans) were May and June. The next in order were the months during the holiday period (July and August). Finally, the following months have seen a gradual decline in the popularity of the system (most likely due to worsening weather conditions).

In the case of April, the analysis is difficult because the system was launched on the 28th of this month.

From the analyst's point of view, the difference in the popularity of the system between typically summer months (July, August) and spring months (May, June) may be interesting. In my opinion, the fewer users in the summer months can be reduced to two main reasons:
1. Summer months are holiday season in Poland, therefore some of the system's users (employees commuting to work) are on holiday away from home.
2. Wroclaw is one of the main academic cities in Poland. During the summer months, most students stay outside Wroclaw (in their hometowns), reducing the number of active system users.

The correctness of the second statement is confirmed after analyzing the most popular user routes (see the chapter [Bike stations analysis](#stations)). The top ten most popular routes included, among others, those leading from the dormitory (docking station: Wróblewskiego (Teki)) to the main building of the Wroclaw University of Technology (docking station: Norwid / Wyspiański (PWr) or to the stations near the main campus (Łukasiewicza / Smoluchowski (PWr), Rondo Regana).

#### Total bike rides by month
![monthAggPlot](images/plots/monthAggPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb#monthAggPlot)

#### Average bike rides by month
![monthAvgPlot](images/plots/monthAvgPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb#monthAvgPlot)

### Total / average bike rides by day of the week
Secondly, the subject of the analysis is the total number of bike rentals on a given day and the average number of rentals per day of the week.

In the case of the total daily number of rentals, the trend described in the previous paragraph can be clearly seen. The peak of the system's popularity falls in May and June, while in the following months a gradual decrease in the number of bicycle rentals is visible.
Also, the graph showing the average number of rentals per weekday shows that bicycles are more popular on business days than on weekends, which may suggest that residents use bicycles mainly as a means of communication on the way to work.

In addition, the daily chart clearly shows 3 days in which the number of rentals clearly deviated from the norm. These are:
1. May 20 (Wednesday);
2. September 6 (Sunday);
3. November 15 (Sunday).

It can be assumed that a clear deviation from the standard in terms of loans (2-3 times smaller than on neighboring days) may be due to a faulty data set for these days i.e. the system saved only a part of the loans that took place on those days.

#### Total bike rides by day of the week
![dayAggPlot](images/plots/dayAggPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb#dayAggPlot)

#### Average bike rides by day of the week
![weekdayAvgPlot](images/plots/weekdayAvgPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb#weekdayAvgPlot)

### Bike rides across time of the day
TThe third type of chart shows how the number of rentals changes depending on the time of day.
The first two charts show the total and the average number of rentals broken down by day of the week. There are two clear tendencies here:
1. on weekdays there are two clear peaks in the number of rents (at 7 and 16 respectively)
2. at weekends the number of rentals is more extended in time and the peak of system reliability falls between 12 and 20.

In connection with the above facts, two conclusions can be drawn:
1. on weekdays, people use bicycles as a means of transport to and from work.
2. on weekends people use the bicycle more for tourism.

The above conclusions are confirmed in the next chart, which shows the use of bicycles on business days and non-working days (weekends and holidays).

Of course, the above conclusions on how to use bicycles should also be confronted with the routes that people choose (this will be the subject of the analysis in the next chapter - [Bike stations analysis](#stations)).

The last graph shows the use of bicycles at specific times of the day, broken down by month. Local peaks can still be clearly seen in the hours when people move from and to work. Nevertheless, it can also be seen how with the following autumn months (September, October, November) these charts are gradually flattening. Most likely, weather conditions have a big impact on this. (this will be the subject of the analysis in the next chapter - [Weather conditions usage patterns](#weather)).

#### Total rentals by the hour and weekday
![hourAggPlot](images/plots/hourAggPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb#hourAggPlot)

#### Average rentals by the hour and weekday
![hourAvgPlot](images/plots/hourAvgPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb#hourAvgPlot)

#### Average rentals by the hour and type of day (working day or weekend/holiday)
![hourAvgWDPlot](images/plots/hourAvgWDPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb#hourAvgWDPlot)

#### Average rentals by the hour and month
![hourAvgMonthPlot](images/plots/hourAvgMonthPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb#hourAvgMonthPlot)

### Bike rides duration
Another factor in the analysis of system users' behavior is the length of trips they make. As you can see in the table below, almost 83.5% of the journey is shorter than 20 minutes, which, according to the terms of service, means that the user does not incur any fees for using the bike. In addition, almost 96% of the journey is less than 60 minutes, while only 1.59% of the rentals last longer than 2 hours.

Given the above, for further analysis, I will limit the data set only to travels that were shorter than 60 minutes.

![durationTable](images/plots/durationTable.png)

The chart below shows the rental time distribution. It clearly shows that the overwhelming number of trips is not more than 30 minutes and reaches its peak between 8 and 12 minutes. Therefore, it should be assumed that the users use the system as a supplement to other means of public transport, i.e. a way to reach or from the main communication node (bus or train station, bus or tram loop). The accuracy of the above statement can be confronted with the analysis of the most popular docking stations (chapter Docking stations) and the most popular routes.

![durationAggPlot](images/plots/durationAggPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb#durationAggPlot)

The next graph presents a breakdown of the time distribution of loans divided into working days and non-working days (weekends and holidays).

![durationWDPlot](images/plots/durationWDPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb#durationWDPlot)

As you can see, both charts do not differ significantly from each other, i.e. short trips dominate in both cases. Nevertheless, it is worth deepening the analysis here and looking at how average travel times for particular types of days.

![averageRentalTimeTable](images/plots/averageRentalTimeTable.png)

The table above clearly shows that the average duration of rentals on weekends is almost 9 minutes longer than on business days. The above results from two facts shown in the charts below, i.e.:

1. the number of trips over 60 minutes on weekends is almost 3 times higher than on business days.
2. total travel time over 60 minutes is almost 2 times greater than on a business day.

Thus, it is clearly visible that on days off, bikes are not only used as a means of public transport, but as a form of recreation.

![durationCountPlot](images/plots/durationCountPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb#durationCountPlot)

![durationTotalPlot](images/plots/durationTotalPlot.png)
[Interactive plot](https://nbviewer.jupyter.org/github/sebastian-konicz/WRM/blob/master/notebooks/reports/RidingPatternsPlots.ipynb#durationTotalPlot)

[Source / Inspiration](https://medium.com/analytics-vidhya/how-to-finish-top-10-percentile-in-bike-sharing-demand-competition-in-kaggle-part-1-c816ea9c51e1)

## Bike stations analysis <a id="stations"></a>
### Map of all docking stations
First of all, below I present to you a map of all the cycle hire stations across Wroclaw and surrounding areas.
I've also generated an interactive version of this plot in folium - click [here](https://sebastian-konicz.github.io/WRM/images/sites/DockingStationsMap.html) to see it. You can zoom/scroll with this version, and it also tells you the name of each location.

![All docking stations](images/final/DockingStationsMap.png)

### Ranking of bike stations
In this chapter, we will analyze the popularity of individual docking stations. The following 3 tables present the top 10 docking stations in terms of:
1. Number of bike rentals from a given station (outflow)
2. Number of bike returns at a given station (inflow)
3. Total bike flow at the station (outflow + inflow).

As you can easily see, the individual tables differ only slightly from each other i.e. the list of stations is unchanged, the difference is only in their order.

A deeper analysis of the locations of the most popular docking stations allows us to divide them into 2 basic categories:
1. stations located in the city center (Rynek, Wita Stwosza - centurm, Fosa Miejska)
2. stations located at the main transport hubs (Rondo Regana, Dworzec Główny, Powstańców Śląskich (Aleja Hallera), Powstańców Śląskich (Arkady Wrocławskie), Plac Jana Pawła II (Akademia Muzyczna), Drobnera / Plac Bema)

A special case is the Szczesliwicka station, which is located at the tallest office building in Wrocław. Therefore, its popularity is due to a large number of employees working in this building.

The last table presents the redistribution mismatch at a given station i.e. difference between the inflows and outflows. This table can be useful for the bike-sharing operator because it shows the stations that are worst affected by this mismatch and thus require the most redistribution of bikes during the day.

#### Most popular bike stations (outflow)
![outflowTable](images/plots/outflowTable.png)

#### Most popular bike stations (inflow)
![inflowTable](images/plots/inflowTable.png)

#### Most popular bike stations (total flow)
![totalflowTable](images/plots/totalflowTable.png)

#### Redistribution mismatch (outflow - inflow)
![flowDiffTable](images/plots/flowDiffTable.png)

### Analysis of flows between stations
The next step in analyzing the patterns connected with docking stations is an analysis of flows between stations. In this chapter, I will concentrate on analyzing patterns during weekdays.
In the images below, orange represents a station with more bikes leaving than coming in (outflows > inflows), whilst blue represents the opposite (outflows < inflows). As expected, in the morning people commute into the center from the suburbs, whilst the opposite occurs in the evening.

#### Net arivals/departures in the morning (working days)
![Net arrivals/departures - morning](images/final/NetArivalsDepartures-morning.png)
[Interactive map](https://sebastian-konicz.github.io/WRM/images/sites/NetArivalsDepartures-morning.html)

#### Net arivals/departures in the afternoon (working days)
![Net arrivals/departures - afternoon](images/final/NetArivalsDepartures-afternoon.png)
[Interactive map](https://sebastian-konicz.github.io/WRM/images/sites/NetArivaslDepartures-afternoon.html)

The animated gifs below show the dynamic change of flows between docking stations during morning and afternoon rush hours on weekdays.

#### Intensity of arivals/departures in the morning (working days)
![Intensity - morning](images/final/IntensityMorning.gif)

#### Intensity of arivals/departures in the afternoon (during weekdays)
![Intensity - afternoon](images/final/IntensityAfternoon.gif)

[Source / Inspiration](https://github.com/charlie1347/TfL_bikes)

### Page rank algorithm
( to be added in the future)

### Network analysis of bike stations
#### Bike paths in Wroclaw
The below images shows all the bike paths that were taken by the system users. As the image is hard to read for a better understanding of bike paths please use the interactive version of the map. The interactive map has multiple layers showing the number of journeys for a given route.
![BikePaths](images/final/BikePaths.png)
[Interactive map](https://sebastian-konicz.github.io/WRM/images/sites/BikePathsMapTreshold.html)

#### Most popular bike paths (outflow)
Furthermore, below I present the table with the top 10 most frequently used routes.
![mostPopTable](images/plots/mostPopTable.png)

It is worth noting (and was already mentioned before) that the top ten most popular routes included, among others, those leading from the dormitories (docking station: Wróblewskiego (Teki) and Plac Grunwaldzki (DS Ołówek)) to the main building of the Wroclaw University of Technology (docking station: Norwid / Wyspiański (PWr) or to the stations near the main campus (Rondo Regana).

The second most popular bike paths are those leading to and from the biggest scyscrapper in Wrocław.

## Weather conditions usage patterns <a id="weather"></a>
In this chapter, I will try to answer the question of how atmospheric conditions affect the popularity of the system. To do that first I have to calculate the correlation coefficient between the number of rides and individual weather factors like temperature, sensed temperature (atemp), precipitation, humidity, and wind speed. The values of individual coefficients are visible in the graph below in the bottom row.

From the table below its visible that only two weather factors have a fairly significant influence (greater than 0,5) on the number of rides:
- temperature / sensed temperature has a positive influence - i.e the higher temperature the more rented bikes;
- humidity has a negative influence - i.e the higher humidity the less rented bikes.

![heatmapDaily](images/plots/heatmapDaily.png)

![plotCorrTemp](images/plots/plotCorrTemp.png)

![plotCorrHum](images/plots/plotCorrHum.png)

[Source / Inspiration](https://towardsdatascience.com/exploring-toronto-bike-share-ridership-using-python-3dc87d35cb62)

## Route predictions <a id="route"></a>
#### Route prediction graph
( to be added in the future)
[Source / Inspiration](https://github.com/charlie1347/TfL_bikes)

## Conclusions <a id="conclusions"></a>
Bearing the above analisys in mind, the following conclusions can be drawn:
- during weekdays people use bike-sharing system as a supplementary means of transport in commuting to and from work/school during the morning and afternoon rush hours
- during weekends and holidays, in addition to the commute, people use bikes as a form of recreation
- the most popular routes and docking stations focus around important communication nodes (train, tram and bus stations)  as well as places with a high concentration of people (universities, scyscrapers and office districts)
- the demand on the bikes is fairly strongly correlated with the atmospheric condition (temerature and humidity) and season of the year

## Project Organization <a id="project"></a>
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical datasets for modeling.
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
