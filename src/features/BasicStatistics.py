import pandas as pd
from pathlib import Path
import geopy.distance as gd
import re
import numpy as np
from datetime import datetime
import datetime
import time

# Plotly and cufflings standart impors
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import cufflinks as cf
cf.go_offline(connected=True)

# Offline mode
import plotly.offline
pio.orca.config

pd.options.display.max_columns = 50

def main(dir):
    print("Loading data")
    RentalData = pd.read_csv(dir + r'\data\processed\RentalData2015Enriched.csv', delimiter=",", encoding="utf-8")

    numberOfBikes = RentalData.groupby("BikeNumber").first()
    numberOfBikes = numberOfBikes['Count'].count()

    numberOfDockingStations = RentalData.groupby("StartStation").first()
    numberOfDockingStations = numberOfDockingStations['Count'].count()

    validRentals = RentalData["Count"].count()
    print(validRentals)

    mostPopularBike = pd.DataFrame(RentalData.groupby("BikeNumber")["Count"].sum()).reset_index()
    mostPopularBike.sort_values(by="Count", ascending=False, inplace=True)
    mostPopularBike = mostPopularBike.iloc[0, 0]
    print(mostPopularBike)

    mostPopularStation = RentalData[["StartStation", "Count"]]
    mostPopularStation = pd.DataFrame(mostPopularStation.groupby("StartStation")['Count'].sum()).reset_index()
    mostPopularStation.sort_values(by="Count", ascending=False, inplace=True)
    mostPopularStation = mostPopularStation.iloc[0, 0]
    print(mostPopularStation)

    mostPopularPath = pd.DataFrame(RentalData.groupby(["StartStation", 'EndStation'])["Count"].sum()).reset_index()
    mostPopularPath = mostPopularPath[mostPopularPath["StartStation"] != mostPopularPath['EndStation']]
    mostPopularPath.sort_values(by="Count", ascending=False, inplace=True)
    mostPopularPath1 = mostPopularPath.iloc[0, 0]
    mostPopularPath2 = mostPopularPath.iloc[0, 1]
    mostPopularPath3 = mostPopularPath.iloc[0, 2]
    mostPopularPath = mostPopularPath1 + " <-> " + mostPopularPath2 + " (" + str(mostPopularPath3) + " rides)"
    print(mostPopularPath)

    averageRentalTime = RentalData["Duration"].mean()
    averageRentalTime = time.strftime("%H:%M:%S", time.gmtime(averageRentalTime))
    print(averageRentalTime)

    averageSpeed = RentalData[RentalData["StartStation"] != RentalData['EndStation']]
    averageSpeed = averageSpeed["Speed"].mean()
    averageSpeed = round(averageSpeed, 2)
    print(averageSpeed)

    recordDay = RentalData[["Date", "Count"]]
    recordDay = pd.DataFrame(recordDay.groupby("Date")['Count'].sum()).reset_index()
    recordDay.sort_values(by="Count", ascending=False, inplace=True)
    recordDay1 = recordDay.iloc[0, 0]
    recordDay2 = recordDay.iloc[0, 1]
    recordDay = recordDay1 + " (" + str(recordDay2) + " rides)"
    print(recordDay)

    recordMonth = RentalData[["Month", "Count"]]
    recordMonth = pd.DataFrame(recordMonth.groupby("Month")['Count'].sum()).reset_index()
    recordMonth.sort_values(by="Count", ascending=False, inplace=True)
    recordMonth1 = recordMonth.iloc[0, 0]
    recordMonth2 = recordMonth.iloc[0, 1]
    recordMonth = recordMonth1 + " (" + str(recordMonth2) + " rides)"
    print(recordMonth)

    # Creating tables
    headerColor = 'black'
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    statisticsTable = go.Figure(data=[go.Table(
        columnwidth=[30, 40],
        header=dict(
            values=['<b>Description</b>', '<b>Result</b>'],
            line_color='black',
            fill_color=headerColor,
            align=['center'],
            font=dict(color='white', size=14),
            height=30
        ),
        cells=dict(
            values=[['number of bikes', 'number of docking stations', 'total number of valid rentals', 'most popular bike',
                     'most popular docking station', 'most popular path', 'average rental time', 'average speed',
                     'record day', 'record month'],
                    [numberOfBikes, numberOfDockingStations, validRentals, mostPopularBike, mostPopularStation,
                     mostPopularPath, averageRentalTime, averageSpeed, recordDay, recordMonth]],
            line_color='darkslategray',
            fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor] * 3],
            align=['left', 'center'],
            font=dict(color='black', size=14),
            height=30
        ))
    ])

    return statisticsTable

def plots(dir):
    # Unpacking return variables from main function
    statisticsTable = main(dir)

    tablesDictionary = {"statisticsTable": statisticsTable}

    for key, value in tablesDictionary.items():
        plotly.offline.plot(value, filename=(dir + r'\images\sites\{}.html'.format(key)))
        go.Figure(value).write_image(dir + r'\images\plots\{}.png'.format(key), width=1280, height=500)

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    plots(project_dir)
    # main(project_dir)

