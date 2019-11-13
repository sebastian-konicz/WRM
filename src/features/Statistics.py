import pylab
import calendar
import numpy as np
import pandas as pd
import seaborn as sn
from scipy import stats
# import missingno as msno
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
from pathlib import Path

# Plotly standart impors
import plotly.graph_objects as go
import plotly.io as pio
import cufflinks as cf
cf.go_offline(connected=True)

# Offline mode
import plotly.offline

pd.options.display.max_columns = 50

def main(dir):
    # # Loading Data Set
    # print("Loading dataset")
    # RentalData = pd.read_csv(dir + r'\data\processed\RentalData2015.csv', delimiter=",", encoding="utf-8")
    #
    # # Setting the national holidays and changing list values to datetime objects
    # NationalHolidays = ["2015-01-01", "2015-01-06", "2015-04-05", "2015-04-06", "2015-05-01", "2015-05-03",
    #                     "2015-05-24", "2015-06-04", "2015-08-15", "2015-11-01", "2015-11-11", "2015-12-25", "2015-12-26"]
    # holidays = []
    # for i in NationalHolidays:
    #     date = pd.to_datetime(i).date()
    #     holidays.append(date)
    #
    # # Creating datatime columns for analysis
    # RentalData["StartDate"] = pd.to_datetime(RentalData["StartDate"])
    # RentalData['Date'] = RentalData["StartDate"].map(lambda x: x.date())
    # RentalData['Hour'] = RentalData["StartDate"].map(lambda x: x.hour)
    # RentalData['Weekday'] = RentalData["StartDate"].map(lambda x: x.weekday())
    # RentalData['Month'] = RentalData["StartDate"].map(lambda x: x.month)
    # RentalData["Holiday"] = RentalData["Date"].isin(holidays)
    # RentalData['Holiday'] = RentalData.apply(lambda RentalData: 1 if (RentalData["Holiday"] is True) else 0, axis=1)
    # RentalData["WorkingDay"] = RentalData.apply(lambda RentalData: 1 if ((RentalData['Weekday'] >= 0) & (RentalData['Weekday'] < 5) & (RentalData['Holiday'] != 1)) else 0, axis=1)
    #
    # # Changing numeric values to text values
    # RentalData["Weekday"] = RentalData["Weekday"].map({0: "Monday", 1: "Tuesday", 2: "Wednesday",
    #                                                   3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"})
    # RentalData["Month"] = RentalData["Month"].map({1: "January", 2: "February", 3: "March", 4: "April",
    #                                                5: "May", 6: "June", 7: "July", 8: "August",
    #                                                9: "September", 10: "October", 11: "November", 12: "December"})
    #
    # # Changing values to category type
    # categoryVariableList = ["Hour", "Weekday", "Month", "WorkingDay"]
    # for var in categoryVariableList:
    #     RentalData[var] = RentalData[var].astype("category")
    #
    # # Adding technical column count
    # RentalData['Count'] = 1
    #
    # print("Saving to Excel")
    # RentalData.to_csv(dir + r'\data\processed\RentalDataRewised.csv', encoding='utf-8', index=False)

    RentalData = pd.read_csv(dir + r'\data\processed\RentalDataRewised.csv', delimiter=",", encoding="utf-8")

    monthOrder = ["April", "May", "June", "July", "August", "September", "October", "November"]
    dayOrder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Plot for total rental by month
    monthAggregated = pd.DataFrame(RentalData.groupby("Month")['Count'].sum()).reset_index()

    monthAggPlotData = [go.Bar(x=monthAggregated['Month'], y=monthAggregated['Count'],
                                marker={'color': monthAggregated['Count'], "autocolorscale": True})]
    monthAggPlotLayout = go.Layout(title=go.layout.Title(text="Total rentals by month"),
                                     xaxis=dict(categoryorder='array', categoryarray=monthOrder))

    monthAggPlot = dict(data=monthAggPlotData, layout=monthAggPlotLayout)
    # monthAggPlot = go.Figure(data=monthAggPlotData, layout=monthAggPlotLayout)

    # plotly.offline.plot(monthAggPlot, filename=(dir + r'\images\sites\monthAggPlot.html'))
    # monthAggPlot.write_image(dir + r'\images\final\monthAggPlot.png')

    # Plot for total rental in particular days by hour of the day
    hourAggregated = pd.DataFrame(RentalData.groupby(["Hour", "Weekday"], sort=True)["Count"].count()).reset_index()
    hourAggPivot = hourAggregated.pivot(index="Hour", columns="Weekday")["Count"]

    # Generating lines for differend day of the week
    hourAggPlotData = []
    for day in dayOrder:
        plotLine = go.Scatter(x=hourAggPivot.index, y=hourAggPivot[day], mode="lines", name=day)
        hourAggPlotData.append(plotLine)

    hourAggPlotLayout = go.Layout(title=go.layout.Title(text="Total rentals by hour and weekday"))
    hourAggPlot = dict(data=hourAggPlotData, layout =hourAggPlotLayout)
    # hourAggPlot = go.Figure(data=hourAggPlotData, layout =hourAggPlotLayout)

    # plotly.offline.plot(hourAggPlot, filename=(dir + r'\images\sites\hourAggPlot.html'))

    # fig, (ax1, ax2) = plt.subplots(nrows=2)
    # monthAggregated = pd.DataFrame(RentalData.groupby("Month")['Count'].sum()).reset_index()
    # print(monthAggregated)
    # monthSorted = monthAggregated.sort_values(by="Count", ascending=False)
    # sn.barplot(data=monthSorted, x="Month", y="Count", ax=ax1, order=sortOrder)
    # ax1.set(xlabel='Month', ylabel='Count', title="Count of rides By Month")
    #
    #
    # hourAggregated = pd.DataFrame(RentalData.groupby(["Hour", "Weekday"], sort=True)["Count"].count()).reset_index()
    # print(hourAggregated)
    # sn.pointplot(x=hourAggregated["Hour"], y=hourAggregated["Count"], hue=hourAggregated["Weekday"],
    #              hue_order=hueOrder, data=hourAggregated, join=True, ax=ax2)
    # ax2.set(xlabel='Hour Of The Day', ylabel='Users Count',
    #         title="Users Count By Hour Of The Day Across Weekdays", label='big')
    #
    # plt.show()

    return monthAggPlot, hourAggPlot, monthAggPlotData


if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir)
