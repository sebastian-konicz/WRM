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
        title=go.layout.Title(text="Average rentals by hour and type of day (working day or weekend/holiday)", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
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

    # Rental duration (all)
    durationAggregated = pd.DataFrame(RentalData.groupby(["Duration"])['Count'].sum()).reset_index()
    durationLimitedAll = durationAggregated['Count'].sum()
    durationLimited120 = durationAggregated[(durationAggregated['Duration'] <= 7200)]
    durationLimited120 = durationLimited120['Count'].sum()
    durationAggregated = durationAggregated[(durationAggregated['Duration'] <= 3600)]
    durationAggregated['Total Duration'] = durationAggregated.apply(lambda durationAggregated: time.strftime("%H:%M:%S", time.gmtime(durationAggregated['Duration'])), axis=1)

    durationAggPlotData = go.Scatter(x=durationAggregated['Total Duration'], y=durationAggregated['Count'], mode="lines")
    durationAggPlotLayout = go.Layout(
        title=go.layout.Title(text="Rental time", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
        template="plotly_dark", xaxis_title="time (hh:mm:ss)", yaxis_title="no. of rentals",
        xaxis=dict(tickmode="array", tickvals=timeVals, ticktext=timeVals))

    durationAggPlot = dict(data=durationAggPlotData, layout=durationAggPlotLayout)

    #Time limits
    durationLimited60 = durationAggregated[(durationAggregated['Duration'] <= 3600)]
    durationLimited60 = durationLimited60['Count'].sum()

    # Rental duration (limited)
    durationLimited = pd.DataFrame(RentalData.groupby(["Duration"])['Count'].sum()).reset_index()
    durationLimited = durationLimited[(durationLimited['Duration'] <= 3600)]
    durationLimited['Total Duration'] = durationLimited.apply(lambda durationLimited: time.strftime("%H:%M:%S", time.gmtime(durationLimited['Duration'])), axis=1)

    durationLtdPlotData = go.Scatter(x=durationLimited['Total Duration'], y=durationLimited['Count'], mode="lines")
    durationLtdPlotLayout = go.Layout(
        title=go.layout.Title(text="Rental time", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
        template="plotly_dark", xaxis_title="time (hh:mm:ss)", yaxis_title="no. of rentals",
        xaxis=dict(tickmode="array", tickvals=timeVals, ticktext=timeVals))

    durationLtdPlot = dict(data=durationLtdPlotData, layout=durationLtdPlotLayout)

    #Time limits
    durationLimited30 = durationLimited[(durationLimited['Duration'] <= 1800)]
    durationLimited30 = durationLimited30['Count'].sum()
    durationLimited20 = durationLimited[(durationLimited['Duration'] <= 1200)]
    durationLimited20 = durationLimited20['Count'].sum()

    # Rental duration on working days
    durationWorkingDay = RentalData[RentalData["WorkingDay"] == "WorkingDay"]
    durationWorkingDay = pd.DataFrame(durationWorkingDay.groupby(["Duration"])["Count"].sum()).reset_index()
    durationWorkingDay = durationWorkingDay[(durationWorkingDay['Duration'] <= 3600)]
    durationWorkingDay['Total Duration'] = durationWorkingDay.apply(
        lambda durationWorkingDay: time.strftime("%H:%M:%S", time.gmtime(durationWorkingDay['Duration'])), axis=1)

    durationWDPlotData = go.Scatter(x=durationWorkingDay['Total Duration'], y=durationWorkingDay['Count'], mode="lines")

    # Rental duration on days off
    durationDayOff = RentalData[RentalData["WorkingDay"] == "DayOff"]
    durationDayOff = pd.DataFrame(durationDayOff.groupby(["Duration"])["Count"].sum()).reset_index()
    durationDayOff = durationDayOff[(durationDayOff['Duration'] <= 3600)]
    durationDayOff['Total Duration'] = durationDayOff.apply(
        lambda durationDayOff: time.strftime("%H:%M:%S", time.gmtime(durationDayOff['Duration'])), axis=1)

    durationDOPlotData = go.Scatter(x=durationDayOff['Total Duration'], y=durationDayOff['Count'], mode="lines")

    durationWDPlotLayout = go.Layout(
        template="plotly_dark", showlegend=False,
        xaxis1=dict(tickmode="array", tickvals=timeVals, ticktext=timeVals, title="time (hh:mm:ss)"), yaxis1=dict(title="no. of rentals"),
        xaxis2=dict(tickmode="array", tickvals=timeVals, ticktext=timeVals, title="time (hh:mm:ss)"), yaxis2=dict(title="no. of rentals"),)

    # Creating subplots duration on working days / days off
    durationWDPlot = make_subplots(rows=2, cols=1, subplot_titles=("Rental time during week days", "Rental time during days off"))

    durationWDPlot.add_trace(durationWDPlotData, row=1, col=1)
    durationWDPlot.add_trace(durationDOPlotData, row=2, col=1)

    durationWDPlot.update_layout(durationWDPlotLayout)

    # Creating table concerning duration time and percent of total rides
    durationPercent20 = str(round(((durationLimited20 / durationLimitedAll) * 100), 2)) + "%"
    durationPercent30 = str(round(((durationLimited30 / durationLimitedAll) * 100), 2)) + "%"
    durationPercent60 = str(round(((durationLimited60 / durationLimitedAll) * 100), 2)) + "%"
    durationPercent120 = str(round(((durationLimited120 / durationLimitedAll) * 100), 2)) + "%"

    headerColor = 'black'
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    durationTable = go.Figure(data=[go.Table(
        columnwidth=[50, 40, 40],
        header=dict(
            values=['<b>time limit</b>', '<b>no. of rides</b>', '<b>% of total rides</b>'],
            line_color='black',
            fill_color=headerColor,
            align=['left', 'center'],
            font=dict(color='white', size=14),
            height=30
        ),
        cells=dict(
            values=[
                ['rides shorter than 20 minutes', 'rides shorter than 60 minutes', 'rides shorter than 120 minutes', '<b>no limit</b>'],
                [durationLimited20, durationLimited60, durationLimited120, "<b>{}</b>".format(durationLimitedAll)],
                [durationPercent20, durationPercent60, durationPercent120, "<b>100,00%</b>"]],
            line_color='darkslategray',
            fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor, rowOddColor]],
            align=['left', 'center'],
            font=dict(color='black', size=14),
            height=25
        ))
    ])

    # Creating table concerning average rental time
    AverageRentalTime = RentalData["Duration"].mean()
    AverageRentalTimeWD = RentalData[RentalData["WorkingDay"] == "WorkingDay"]
    AverageRentalTimeWD = AverageRentalTimeWD["Duration"].mean()
    AverageRentalTimeDO = RentalData[RentalData["WorkingDay"] == "DayOff"]
    AverageRentalTimeDO = AverageRentalTimeDO["Duration"].mean()

    AverageRentalTime = time.strftime("%H:%M:%S", time.gmtime(AverageRentalTime))
    AverageRentalTimeWD = time.strftime("%H:%M:%S", time.gmtime(AverageRentalTimeWD))
    AverageRentalTimeDO = time.strftime("%H:%M:%S", time.gmtime(AverageRentalTimeDO))

    averageRentalTimeTable = go.Figure(data=[go.Table(
        columnwidth=[50, 40],
        header=dict(
            values=['<b>Type of day</b>', '<b>average time</b>'],
            line_color='black',
            fill_color=headerColor,
            align=['left', 'center'],
            font=dict(color='white', size=14),
            height=30
        ),
        cells=dict(
            values=[
                ['Week day', 'Day off', '<b>All days</b>'],
                [AverageRentalTimeWD, AverageRentalTimeDO, "<b>{}</b>".format(AverageRentalTime)]],
            line_color='darkslategray',
            fill_color=[[rowOddColor, rowEvenColor, rowOddColor]],
            align=['left', 'center'],
            font=dict(color='black', size=14),
            height=25
        ))
    ])

    # Calculating rental time for working day
    # Count
    durationWD = RentalData[RentalData["WorkingDay"] == "WorkingDay"]
    durationWDAllRental = durationWD['Count'].sum()
    durationWDLongRental = durationWD[(durationWD['Duration'] > 3600)]
    durationWDLongRental = durationWDLongRental['Count'].sum()
    durationWDShortRental = durationWD[(durationWD['Duration'] <= 3600)]
    durationWDShortRental = durationWDShortRental['Count'].sum()

    # Total duration
    durationWDAllRentalTotal = durationWD['Duration'].sum()
    durationWDLongRentalTotal = durationWD[(durationWD['Duration'] > 3600)]
    durationWDLongRentalTotal = durationWDLongRentalTotal['Duration'].sum()
    durationWDShortRentalTotal = durationWD[(durationWD['Duration'] <= 3600)]
    durationWDShortRentalTotal = durationWDShortRentalTotal['Duration'].sum()

    # Calculating rental time for working day
    # Count
    durationDO = RentalData[RentalData["WorkingDay"] == "DayOff"]
    durationDOAllRental = durationDO['Count'].sum()
    durationDOLongRental = durationDO[(durationDO['Duration'] > 3600)]
    durationDOLongRental = durationDOLongRental['Count'].sum()
    durationDOShortRental = durationDO[(durationDO['Duration'] <= 3600)]
    durationDOShortRental = durationDOShortRental['Count'].sum()
    # Total duration
    durationDOAllRentalTotal = durationDO['Duration'].sum()
    durationDOLongRentalTotal = durationDO[(durationDO['Duration'] > 3600)]
    durationDOLongRentalTotal = durationDOLongRentalTotal['Duration'].sum()
    durationDOShortRentalTotal = durationDO[(durationDO['Duration'] <= 3600)]
    durationDOShortRentalTotal = durationDOShortRentalTotal['Duration'].sum()

    # Pie chart - duration count
    durationWDCountLabels = ['Short Rental (<60 min)', 'Long Rental (>60 min)']
    durationWDCountValues = [durationWDShortRental, durationWDLongRental]

    durationDOCountLabels = ['Short Rental (<60 min)', 'Long Rental (>60 min)']
    durationDOCountValues = [durationDOShortRental, durationDOLongRental]

    durationWDCount = go.Pie(labels=durationWDCountLabels, values=durationWDCountValues, pull=[0, 0.2])
    durationDOCount = go.Pie(labels=durationDOCountLabels, values=durationDOCountValues, pull=[0, 0.2])

    durationCountPlotLayout = go.Layout(template="plotly_dark", title=go.layout.Title(text="Total no. of rentals", x=0.5, y=0.95, xanchor='center', yanchor='middle'))

    # Creating subplots duration on working days / days off
    durationCountPlot = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]], subplot_titles=("week days", "days off"))

    durationCountPlot.add_trace(durationWDCount, 1, 1)
    durationCountPlot.add_trace(durationDOCount, 1, 2)

    durationCountPlot.update_layout(durationCountPlotLayout)

    # Pie chart - duration total time
    durationWDTotalLabels = ['Short Rental (<60 min)', 'Long Rental (>60 min)']
    durationWDTotalValues = [durationWDShortRentalTotal, durationWDLongRentalTotal]

    durationDOTotalLabels = ['Short Rental (<60 min)', 'Long Rental (>60 min)']
    durationDOTotalValues = [durationDOShortRentalTotal, durationDOLongRentalTotal]

    durationWDTotal = go.Pie(labels=durationWDTotalLabels, values=durationWDTotalValues, pull=[0, 0.2])
    durationDOTotal = go.Pie(labels=durationDOTotalLabels, values=durationDOTotalValues, pull=[0, 0.2])

    durationTotalPlotLayout = go.Layout(template="plotly_dark", title=go.layout.Title(text="Total rental time", x=0.5, y=0.95, xanchor='center', yanchor='middle'))

    # Creating subplots duration on working days / days off
    durationTotalPlot = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]], subplot_titles=("week days", "days off"))

    durationTotalPlot.add_trace(durationWDTotal, 1, 1)
    durationTotalPlot.add_trace(durationDOTotal, 1, 2)

    durationTotalPlot.update_layout(durationTotalPlotLayout)

    return monthAggPlot, monthAvgPlot, dayAggPlot, weekdayAvgPlot, hourAggPlot, hourAvgPlot, hourAvgWDPlot, hourAvgMonthPlot, durationAggPlot, durationLtdPlot, durationWDPlot, durationTable, durationCountPlot, durationTotalPlot, averageRentalTimeTable

def plots(dir):
    # Unpacking return variables from main function
    monthAggPlot, monthAvgPlot, dayAggPlot, weekdayAvgPlot, hourAggPlot, hourAvgPlot, hourAvgWDPlot, hourAvgMonthPlot, durationAggPlot, durationLtdPlot, durationWDPlot, durationTable, durationCountPlot, durationTotalPlot, averageRentalTimeTable = main(dir)

    plotsDictionary = {"monthAggPlot": monthAggPlot, "monthAvgPlot": monthAvgPlot, "dayAggPlot": dayAggPlot,
                       "weekdayAvgPlot": weekdayAvgPlot, "hourAggPlot": hourAggPlot,
                       "hourAvgPlot": hourAvgPlot, "hourAvgWDPlot": hourAvgWDPlot, "hourAvgMonthPlot": hourAvgMonthPlot,
                       "durationAggPlot": durationAggPlot, "durationLtdPlot": durationLtdPlot, "durationWDPlot": durationWDPlot,
                       "durationCountPlot": durationCountPlot, "durationTotalPlot": durationTotalPlot}

    tablesDictionary = {"durationTable": durationTable, "averageRentalTimeTable": averageRentalTimeTable}

    for key, value in plotsDictionary.items():
        plotly.offline.plot(value, filename=(dir + r'\images\sites\{}.html'.format(key)))
        go.Figure(value).write_image(dir + r'\images\plots\{}.png'.format(key), width=1280, height=640)

    for key, value in tablesDictionary.items():
        plotly.offline.plot(value, filename=(dir + r'\images\sites\{}.html'.format(key)))
        go.Figure(value).write_image(dir + r'\images\plots\{}.png'.format(key), width=1280, height=350)

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    plots(project_dir)
    # main(project_dir)

