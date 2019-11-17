import pandas as pd
from pathlib import Path
import re
from datetime import datetime

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
    RentalData = pd.read_csv(dir + r'\data\processed\RentalData2015Rewised.csv', delimiter=",", encoding="utf-8")

    monthOrder = ["April", "May", "June", "July", "August", "September", "October", "November"]
    dayOrder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    workingDay = ["WorkingDay", "DayOff"]

    # Plot for total rental by month
    monthAggregated = pd.DataFrame(RentalData.groupby("Month")['Count'].sum()).reset_index()
    monthAggPlotData = go.Bar(x=monthAggregated['Month'], y=monthAggregated['Count'],
                                marker={'color': monthAggregated['Count'], "autocolorscale": True})
    monthAggPlotLayout = go.Layout(title=go.layout.Title(text="Total rentals by month", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
                                   template="plotly_dark", xaxis=dict(categoryorder='array', categoryarray=monthOrder))
    monthAggPlot = dict(data=monthAggPlotData, layout=monthAggPlotLayout)

    # Plot for average rental by month
    monthAverage = pd.DataFrame(RentalData.groupby(["Month", "Date"])['Count'].sum()).reset_index()
    monthAverage = pd.DataFrame(monthAverage.groupby("Month")['Count'].mean()).reset_index()
    monthAvgPlotData = go.Bar(x=monthAverage['Month'], y=monthAverage['Count'],
                                marker={'color': monthAggregated['Count'], "autocolorscale": True})
    monthAvgPlotLayout = go.Layout(title=go.layout.Title(text="Average rentals by month", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
                                   template="plotly_dark", xaxis=dict(categoryorder='array', categoryarray=monthOrder))
    monthAvgPlot = dict(data=monthAvgPlotData, layout=monthAvgPlotLayout)

    # Plot for total rentals by day
    dayAggregated = pd.DataFrame(RentalData.groupby("Date")['Count'].sum()).reset_index()
    dayAggPlotData = go.Bar(x=dayAggregated['Date'], y=dayAggregated['Count'])
    dayAggPlotLayout = go.Layout(title=go.layout.Title(text="Total rentals by day", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
                                 template="plotly_dark")
    dayAggPlot = dict(data=dayAggPlotData, layout=dayAggPlotLayout)

    # Plot for tota; rentals by day of the week
    weekdayAggregated = pd.DataFrame(RentalData.groupby("Weekday")['Count'].sum()).reset_index()
    weekdayAggPlotData = go.Bar(x=weekdayAggregated['Weekday'], y=weekdayAggregated['Count'],
                                marker={'color': weekdayAggregated['Count'], "autocolorscale": True})
    weekdayAggPlotLayout = go.Layout(title=go.layout.Title(text="Total rentals by day of the week", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
                                   template="plotly_dark", xaxis=dict(categoryorder='array', categoryarray=dayOrder))
    weekdayAggPlot = dict(data=weekdayAggPlotData, layout=weekdayAggPlotLayout)

    # Plot for average rentals by day of the week
    weekdayAverage = pd.DataFrame(RentalData.groupby(["Date", "Weekday"])['Count'].sum()).reset_index()
    weekdayAverage = pd.DataFrame(weekdayAverage.groupby("Weekday")['Count'].mean()).reset_index()
    weekdayAvgPlotData = go.Bar(x=weekdayAverage['Weekday'], y=weekdayAverage['Count'],
                                marker={'color': weekdayAverage['Count'], "autocolorscale": True})
    weekdayAvgPlotLayout = go.Layout(title=go.layout.Title(text="Average rentals by day of the week", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
                                   template="plotly_dark", xaxis=dict(categoryorder='array', categoryarray=dayOrder))
    weekdayAvgPlot = dict(data=weekdayAvgPlotData, layout=weekdayAvgPlotLayout)

    # Plot for total rental in particular days by hour of the day
    hourAggregated = pd.DataFrame(RentalData.groupby(["Hour", "Weekday"], sort=True)["Count"].count()).reset_index()
    hourAggPivot = hourAggregated.pivot(index="Hour", columns="Weekday")["Count"]

    # Generating lines for different day of the week
    hourAggPlotData = []
    for day in dayOrder:
        plotLine = go.Scatter(x=hourAggPivot.index, y=hourAggPivot[day], mode="lines", name=day)
        hourAggPlotData.append(plotLine)

    hourAggPlotLayout = go.Layout(title=go.layout.Title(text="Total rentals by hour and weekday", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
                                  template="plotly_dark")
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

    hourAvgPlotLayout = go.Layout(title=go.layout.Title(text="Average rentals by hour and weekday", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
                                  template="plotly_dark")
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

    hourAvgWDPlotLayout = go.Layout(title=go.layout.Title(text="Average rentals by hour and kind of day (working day or weekend/holiday)",
                                                          x=0.5, y=0.9, xanchor='center', yanchor='middle'), template="plotly_dark")
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
        title=go.layout.Title(text="Average rentals by hour and month", x=0.5, y=0.9, xanchor='center', yanchor='middle'), template="plotly_dark")
    hourAvgMonthPlot = dict(data=hourAvgMonthPlotData, layout=hourAvgMonthPlotLayout)

    # Histogram for rentals duration
    RentalData["StartDate"] = pd.to_datetime(RentalData["StartDate"])
    RentalData["EndDate"] = pd.to_datetime(RentalData["EndDate"])
    RentalData['Duration1'] = RentalData.apply(lambda RentalData: RentalData['EndDate'] - RentalData['StartDate'], axis=1)
    RentalData['Duration1'] = RentalData.apply(lambda RentalData: int((RentalData['Duration1'].total_seconds()) / 60), axis=1)
    LongRentals = RentalData[RentalData['Duration1'] > 120]
    ShortRentals = RentalData[RentalData['Duration1'] < 120]
    LongRentals = LongRentals.reset_index(drop=True)
    ShortRentals = ShortRentals.reset_index(drop=True)
    print(ShortRentals['Duration1'])
    print(LongRentals['Duration1'])
    durationAggregated = pd.DataFrame(RentalData.groupby(["Duration1"])['Count'].sum()).reset_index()
    durationAggregated = durationAggregated[(durationAggregated['Duration1'] <= 120) & (durationAggregated['Duration1'] > 0)]
    durationAggregated.to_csv(dir + r'\data\processed\durationAggregated1.csv', encoding='utf-8', index=False)
    durationAggPlotData = go.Histogram(x=durationAggregated['Duration1'], y=durationAggregated['Count'])
    durationAggPlotLayout = go.Layout(title=go.layout.Title(text="Rental Time", x=0.5, y=0.9, xanchor='center', yanchor='middle'),
                                   template="plotly_dark")
    durationAggPlot = dict(data=durationAggPlotData, layout=durationAggPlotLayout)

    return monthAggPlot, monthAvgPlot, dayAggPlot, weekdayAggPlot, weekdayAvgPlot, hourAggPlot, hourAvgPlot, hourAvgWDPlot, hourAvgMonthPlot, durationAggPlot

def graphs(dir):
    # Unpacking return variables from main function
    monthAggPlot, monthAvgPlot, dayAggPlot, weekdayAggPlot, weekdayAvgPlot, hourAggPlot, hourAvgPlot, hourAvgWDPlot, hourAvgMonthPlot, durationAggPlot = main(dir)

    plotsDictionary = {"monthAggPlot": monthAggPlot, "monthAvgPlot": monthAvgPlot, "dayAggPlot": dayAggPlot,
                       "weekdayAggPlot": weekdayAggPlot, "weekdayAvgPlot": weekdayAvgPlot, "hourAggPlot": hourAggPlot,
                       "hourAvgPlot": hourAvgPlot, "hourAvgWDPlot": hourAvgWDPlot,
                       "hourAvgMonthPlot": hourAvgMonthPlot}

    # for key, value in plotsDictionary.items():
    #     plotly.offline.plot(value, filename=(dir + r'\images\sites\{}.html'.format(key)))
    #     go.Figure(value).write_image(dir + r'\images\plots\{}.png'.format(key), width=1280, height=640)
    plotly.offline.plot(durationAggPlot, filename=(dir + r'\images\sites\durationAggPlot.html'))

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    graphs(project_dir)
    # main(project_dir)

