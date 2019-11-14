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
    # RentalData["WorkingDay"] = RentalData["WorkingDay"].map({0: "DayOff", 1: "WorkingDay"})
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

    print("Loading data")
    RentalData = pd.read_csv(dir + r'\data\processed\RentalDataRewised.csv', delimiter=",", encoding="utf-8")

    monthOrder = ["April", "May", "June", "July", "August", "September", "October", "November"]
    dayOrder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    workingDay = ["WorkingDay", "DayOff"]

    # Plot for total rental by month
    monthAggregated = pd.DataFrame(RentalData.groupby("Month")['Count'].sum()).reset_index()
    monthAggPlotData = go.Bar(x=monthAggregated['Month'], y=monthAggregated['Count'],
                                marker={'color': monthAggregated['Count'], "autocolorscale": True})
    monthAggPlotLayout = go.Layout(title=go.layout.Title(text="Total rentals by month"),
                                     xaxis=dict(categoryorder='array', categoryarray=monthOrder))
    monthAggPlot = dict(data=monthAggPlotData, layout=monthAggPlotLayout)

    # Plot for average rental by month
    monthAverage = pd.DataFrame(RentalData.groupby(["Month", "Date"])['Count'].sum()).reset_index()
    monthAverage = pd.DataFrame(monthAverage.groupby("Month")['Count'].mean()).reset_index()
    monthAvgPlotData = go.Bar(x=monthAverage['Month'], y=monthAverage['Count'],
                                marker={'color': monthAggregated['Count'], "autocolorscale": True})
    monthAvgPlotLayout = go.Layout(title=go.layout.Title(text="Average rentals by month"),
                                     xaxis=dict(categoryorder='array', categoryarray=monthOrder))
    monthAvgPlot = dict(data=monthAvgPlotData, layout=monthAvgPlotLayout)

    # Plot for total rentals by day
    dayAggregated = pd.DataFrame(RentalData.groupby("Date")['Count'].sum()).reset_index()
    dayAggPlotData = go.Bar(x=dayAggregated['Date'], y=dayAggregated['Count'])
    dayAggPlotLayout = go.Layout(title=go.layout.Title(text="Total rentals by day"))
    dayAggPlot = dict(data=dayAggPlotData, layout=dayAggPlotLayout)

    # Plot for total rental in particular days by hour of the day
    hourAggregated = pd.DataFrame(RentalData.groupby(["Hour", "Weekday"], sort=True)["Count"].count()).reset_index()
    hourAggPivot = hourAggregated.pivot(index="Hour", columns="Weekday")["Count"]

    # Generating lines for different day of the week
    hourAggPlotData = []
    for day in dayOrder:
        plotLine = go.Scatter(x=hourAggPivot.index, y=hourAggPivot[day], mode="lines", name=day)
        hourAggPlotData.append(plotLine)

    hourAggPlotLayout = go.Layout(title=go.layout.Title(text="Total rentals by hour and weekday"))
    hourAggPlot = dict(data=hourAggPlotData, layout =hourAggPlotLayout)

    # Plot for average rental in particular days by hour of the day
    hourAverage = pd.DataFrame(RentalData.groupby(["Hour", "Date", "Weekday"], sort=True)["Count"].count()).reset_index()
    hourAverage = pd.DataFrame(hourAverage.groupby(["Hour", "Weekday"], sort=True)["Count"].mean()).reset_index()
    hourAvgPivot = hourAverage.pivot(index="Hour", columns="Weekday")["Count"]

    # Generating lines for differend day of the week
    hourAvgPlotData = []
    for day in dayOrder:
        plotLine = go.Scatter(x=hourAvgPivot.index, y=hourAvgPivot[day], mode="lines", name=day)
        hourAvgPlotData.append(plotLine)

    hourAvgPlotLayout = go.Layout(title=go.layout.Title(text="Total rentals by hour and weekday"))
    hourAvgPlot = dict(data=hourAvgPlotData, layout=hourAvgPlotLayout)

    # Plot for average rental in working days or days off by hour of the day
    hourAverageWD = pd.DataFrame(RentalData.groupby(["Hour", "Date", "WorkingDay"], sort=True)["Count"].count()).reset_index()
    hourAverageWD = pd.DataFrame(hourAverageWD.groupby(["Hour", "WorkingDay"], sort=True)["Count"].mean()).reset_index()
    hourAvgPivotWD = hourAverageWD.pivot(index="Hour", columns="WorkingDay")["Count"]

    # Generating lines for differend day of the week
    hourAvgWDPlotData = []
    for day in workingDay:
        plotLine = go.Scatter(x=hourAvgPivotWD.index, y=hourAvgPivotWD[day], mode="lines", name=day)
        hourAvgWDPlotData.append(plotLine)

    hourAvgWDPlotLayout = go.Layout(title=go.layout.Title(text="Average rentals by hour and kind of day (working day or weekend/holiday)"))
    hourAvgWDPlot = dict(data=hourAvgWDPlotData, layout=hourAvgWDPlotLayout)

    # Plot for average rental during particular mont by hour of the day
    hourAverageMonth = pd.DataFrame(RentalData.groupby(["Hour", "Date", "Month"], sort=True)["Count"].count()).reset_index()
    hourAverageMonth = pd.DataFrame(hourAverageMonth.groupby(["Hour", "Month"], sort=True)["Count"].mean()).reset_index()
    hourAvgPivotMonth = hourAverageMonth.pivot(index="Hour", columns="Month")["Count"]

    # Generating lines for differend day of the week
    hourAvgMonthPlotData = []
    for month in monthOrder:
        plotLine = go.Scatter(x=hourAvgPivotMonth.index, y=hourAvgPivotMonth[month], mode="lines", name=month)
        hourAvgMonthPlotData.append(plotLine)

    hourAvgMonthPlotLayout = go.Layout(
        title=go.layout.Title(text="Average rentals by hour and month"))
    hourAvgMonthPlot = dict(data=hourAvgMonthPlotData, layout=hourAvgMonthPlotLayout)

    return monthAggPlot, monthAvgPlot, dayAggPlot, hourAggPlot, hourAvgPlot, hourAvgWDPlot, hourAvgMonthPlot

def graphs(dir):
    monthAggPlot, monthAvgPlot, dayAggPlot, hourAggPlot, hourAvgPlot, hourAvgWDPlot, hourAvgMonthPlot = main(dir)
    plotly.offline.plot(monthAggPlot, filename=(dir + r'\images\sites\monthAggPlot.html'))
    plotly.offline.plot(monthAvgPlot, filename=(dir + r'\images\sites\monthAvgPlot.html'))
    plotly.offline.plot(dayAggPlot, filename=(dir + r'\images\sites\dayAggPlot.html'))
    plotly.offline.plot(hourAggPlot, filename=(dir + r'\images\sites\hourAggPlot.html'))
    plotly.offline.plot(hourAvgPlot, filename=(dir + r'\images\sites\hourAvgPlot.html'))
    plotly.offline.plot(hourAvgWDPlot, filename=(dir + r'\images\sites\hourAvgWDPlot.html'))
    plotly.offline.plot(hourAvgMonthPlot, filename=(dir + r'\images\sites\hourAvgMonthPlot.html'))

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    graphs(project_dir)
    # main(project_dir)

