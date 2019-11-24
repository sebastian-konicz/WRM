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
import cufflinks as cf
cf.go_offline(connected=True)

# Offline mode
import plotly.offline
pio.orca.config

pd.options.display.max_columns = 50

def main(dir):
    print("Loading data")
    RentalData = pd.read_csv(dir + r'\data\processed\RentalData2015Enriched.csv', delimiter=",", encoding="utf-8")

    monthOrder = ["April", "May", "June", "July", "August", "September", "October", "November"]
    dayOrder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    workingDay = ["WorkingDay", "DayOff"]
    hourVals = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    hourText = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00",
                "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]

    timeVals = []
    for i in range(0, 19):
        minutes = (i * 5) % 60
        hour = int((i * 5) / 60)
        timeValue = str(datetime.time(hour=hour, minute=minutes, second=0))
        timeVals.append(timeValue)

    # Plot for total rental by month
    monthAggregated = pd.DataFrame(RentalData.groupby("Month")['Count'].sum()).reset_index()
    monthAggPlotData = go.Bar(x=monthAggregated['Month'], y=monthAggregated['Count'],
                                marker={'color': monthAggregated['Count'], "autocolorscale": True})
    monthAggPlotLayout = go.Layout(title=go.layout.Title(text="Total rentals by month", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
                                   template="plotly_dark", xaxis=dict(categoryorder='array', categoryarray=monthOrder),
                                   xaxis_title="month", yaxis_title="no. of rentals")
    monthAggPlot = dict(data=monthAggPlotData, layout=monthAggPlotLayout)

    # Plot for average rental by month
    monthAverage = pd.DataFrame(RentalData.groupby(["Month", "Date"])['Count'].sum()).reset_index()
    monthAverage = pd.DataFrame(monthAverage.groupby("Month")['Count'].mean()).reset_index()
    monthAvgPlotData = go.Bar(x=monthAverage['Month'], y=monthAverage['Count'],
                                marker={'color': monthAggregated['Count'], "autocolorscale": True})
    monthAvgPlotLayout = go.Layout(title=go.layout.Title(text="Average rentals by month", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
                                   template="plotly_dark", xaxis=dict(categoryorder='array', categoryarray=monthOrder),
                                   xaxis_title="month", yaxis_title="no. of rentals")
    monthAvgPlot = dict(data=monthAvgPlotData, layout=monthAvgPlotLayout)

    # Plot for total rentals by day
    dayAggregated = pd.DataFrame(RentalData.groupby("Date")['Count'].sum()).reset_index()
    dayAggPlotData = go.Bar(x=dayAggregated['Date'], y=dayAggregated['Count'])
    dayAggPlotLayout = go.Layout(title=go.layout.Title(text="Total rentals by day", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
                                 template="plotly_dark", xaxis_title="day", yaxis_title="no. of rentals")
    dayAggPlot = dict(data=dayAggPlotData, layout=dayAggPlotLayout)

    # Plot for average rentals by day of the week
    weekdayAverage = pd.DataFrame(RentalData.groupby(["Date", "Weekday"])['Count'].sum()).reset_index()
    weekdayAverage = pd.DataFrame(weekdayAverage.groupby("Weekday")['Count'].mean()).reset_index()
    weekdayAvgPlotData = go.Bar(x=weekdayAverage['Weekday'], y=weekdayAverage['Count'],
                                marker={'color': weekdayAverage['Count'], "autocolorscale": True})
    weekdayAvgPlotLayout = go.Layout(title=go.layout.Title(text="Average rentals by day of the week", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
                                     template="plotly_dark", xaxis=dict(categoryorder='array', categoryarray=dayOrder),
                                     xaxis_title="month", yaxis_title="no. of rentals")
    weekdayAvgPlot = dict(data=weekdayAvgPlotData, layout=weekdayAvgPlotLayout)

    # Plot for total rental in particular days by hour of the day
    hourAggregated = pd.DataFrame(RentalData.groupby(["Hour", "Weekday"], sort=True)["Count"].count()).reset_index()
    hourAggPivot = hourAggregated.pivot(index="Hour", columns="Weekday")["Count"]

    # Generating lines for different day of the week
    hourAggPlotData = []
    for day in dayOrder:
        plotLine = go.Scatter(x=hourAggPivot.index, y=hourAggPivot[day], mode="lines", name=day)
        hourAggPlotData.append(plotLine)

    hourAggPlotLayout = go.Layout(
        title=go.layout.Title(text="Total rentals by hour and weekday", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
        template="plotly_dark", xaxis_title="hour of day", yaxis_title="no. of rentals",
        xaxis=dict(tickmode="array", tickvals=hourVals, ticktext=hourText))
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

    hourAvgPlotLayout = go.Layout(
        title=go.layout.Title(text="Average rentals by hour and weekday", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
        template="plotly_dark", xaxis_title="hour of day", yaxis_title="no. of rentals",
        xaxis=dict(tickmode="array", tickvals=hourVals, ticktext=hourText))
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

    hourAvgWDPlotLayout = go.Layout(
        title=go.layout.Title(text="Average rentals by hour and kind of day (working day or weekend/holiday)", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
        template="plotly_dark", xaxis_title="hour of day", yaxis_title="no. of rentals",
        xaxis=dict(tickmode="array", tickvals=hourVals, ticktext=hourText))
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
        title=go.layout.Title(text="Average rentals by hour and month", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
        template="plotly_dark", xaxis_title="hour of day", yaxis_title="no. of rentals",
        xaxis=dict(tickmode="array", tickvals=hourVals, ticktext=hourText))
    hourAvgMonthPlot = dict(data=hourAvgMonthPlotData, layout=hourAvgMonthPlotLayout)

    # Rental duration
    durationAggregated = pd.DataFrame(RentalData.groupby(["Duration"])['Count'].sum()).reset_index()
    durationAggregated = durationAggregated[(durationAggregated['Duration'] <= 5400)]
    durationAggregated['Total Duration'] = durationAggregated.apply(lambda durationAggregated: time.strftime("%H:%M:%S", time.gmtime(durationAggregated['Duration'])), axis=1)

    durationAggPlotData = go.Scatter(x=durationAggregated['Total Duration'], y=durationAggregated['Count'], mode="lines")
    durationAggPlotLayout = go.Layout(
        title=go.layout.Title(text="Rental time", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
        template="plotly_dark", xaxis_title="time (hh:mm:ss)", yaxis_title="no. of rentals",
        xaxis=dict(tickmode="array", tickvals=timeVals, ticktext=timeVals))

    durationAggPlot = dict(data=durationAggPlotData, layout=durationAggPlotLayout)

    # # Rental duration average
    # durationAggregated = pd.DataFrame(RentalData.groupby(["Duration"])['Count'].sum()).reset_index()
    # durationAggregated = durationAggregated[(durationAggregated['Duration'] <= 5400)]
    # durationAggregated['Total Duration'] = durationAggregated.apply(lambda durationAggregated: time.strftime("%H:%M:%S", time.gmtime(durationAggregated['Duration'])), axis=1)
    #
    # durationAggPlotData = go.Scatter(x=durationAggregated['Total Duration'], y=durationAggregated['Count'], mode="lines")
    # durationAggPlotLayout = go.Layout(
    #     title=go.layout.Title(text="Rental time", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
    #     template="plotly_dark", xaxis_title="time (hh:mm:ss)", yaxis_title="no. of rentals",
    #     xaxis=dict(tickmode="array", tickvals=timeVals, ticktext=timeVals))
    #
    # durationAggPlot = dict(data=durationAggPlotData, layout=durationAggPlotLayout)


    return monthAggPlot, monthAvgPlot, dayAggPlot, weekdayAvgPlot, hourAggPlot, hourAvgPlot, hourAvgWDPlot, hourAvgMonthPlot, durationAggPlot

def plots(dir):
    # Unpacking return variables from main function
    monthAggPlot, monthAvgPlot, dayAggPlot, weekdayAvgPlot, hourAggPlot, hourAvgPlot, hourAvgWDPlot, hourAvgMonthPlot, durationAggPlot = main(dir)

    plotsDictionary = {"monthAggPlot": monthAggPlot, "monthAvgPlot": monthAvgPlot, "dayAggPlot": dayAggPlot,
                       "weekdayAvgPlot": weekdayAvgPlot, "hourAggPlot": hourAggPlot,
                       "hourAvgPlot": hourAvgPlot, "hourAvgWDPlot": hourAvgWDPlot, "hourAvgMonthPlot": hourAvgMonthPlot,
                       "durationAggPlot": durationAggPlot}

    for key, value in plotsDictionary.items():
        plotly.offline.plot(value, filename=(dir + r'\images\sites\{}.html'.format(key)))
        go.Figure(value).write_image(dir + r'\images\plots\{}.png'.format(key), width=1280, height=640)

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    plots(project_dir)
    # main(project_dir)

