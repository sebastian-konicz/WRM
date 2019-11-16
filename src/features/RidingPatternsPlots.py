import pandas as pd
from pathlib import Path

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
    monthAggPlotLayout = go.Layout(title=go.layout.Title(text="Total rentals by month"), template="plotly_dark",
                                     xaxis=dict(categoryorder='array', categoryarray=monthOrder))
    monthAggPlot = dict(data=monthAggPlotData, layout=monthAggPlotLayout)

    # Plot for average rental by month
    monthAverage = pd.DataFrame(RentalData.groupby(["Month", "Date"])['Count'].sum()).reset_index()
    monthAverage = pd.DataFrame(monthAverage.groupby("Month")['Count'].mean()).reset_index()
    monthAvgPlotData = go.Bar(x=monthAverage['Month'], y=monthAverage['Count'],
                                marker={'color': monthAggregated['Count'], "autocolorscale": True})
    monthAvgPlotLayout = go.Layout(title=go.layout.Title(text="Average rentals by month"), template="plotly_dark",
                                     xaxis=dict(categoryorder='array', categoryarray=monthOrder))
    monthAvgPlot = dict(data=monthAvgPlotData, layout=monthAvgPlotLayout)

    # Plot for total rentals by day
    dayAggregated = pd.DataFrame(RentalData.groupby("Date")['Count'].sum()).reset_index()
    dayAggPlotData = go.Bar(x=dayAggregated['Date'], y=dayAggregated['Count'])
    dayAggPlotLayout = go.Layout(title=go.layout.Title(text="Total rentals by day"), template="plotly_dark")
    dayAggPlot = dict(data=dayAggPlotData, layout=dayAggPlotLayout)

    # Plot for total rental in particular days by hour of the day
    hourAggregated = pd.DataFrame(RentalData.groupby(["Hour", "Weekday"], sort=True)["Count"].count()).reset_index()
    hourAggPivot = hourAggregated.pivot(index="Hour", columns="Weekday")["Count"]

    # Generating lines for different day of the week
    hourAggPlotData = []
    for day in dayOrder:
        plotLine = go.Scatter(x=hourAggPivot.index, y=hourAggPivot[day], mode="lines", name=day)
        hourAggPlotData.append(plotLine)

    hourAggPlotLayout = go.Layout(title=go.layout.Title(text="Total rentals by hour and weekday"), template="plotly_dark")
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

    hourAvgPlotLayout = go.Layout(title=go.layout.Title(text="Average rentals by hour and weekday"), template="plotly_dark")
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

    hourAvgWDPlotLayout = go.Layout(title=go.layout.Title(text="Average rentals by hour and kind of day (working day or weekend/holiday)"),
                                    template="plotly_dark")
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
        title=go.layout.Title(text="Average rentals by hour and month"), template="plotly_dark")
    hourAvgMonthPlot = dict(data=hourAvgMonthPlotData, layout=hourAvgMonthPlotLayout)

    return monthAggPlot, monthAvgPlot, dayAggPlot, hourAggPlot, hourAvgPlot, hourAvgWDPlot, hourAvgMonthPlot

def graphs(dir):
    # Unpacking return variables from main function
    monthAggPlot, monthAvgPlot, dayAggPlot, hourAggPlot, hourAvgPlot, hourAvgWDPlot, hourAvgMonthPlot = main(dir)

    plotsDictionary = {"monthAggPlot": monthAggPlot, "monthAvgPlot": monthAvgPlot, "dayAggPlot": dayAggPlot,
                       "hourAggPlot": hourAggPlot, "hourAvgPlot": hourAvgPlot, "hourAvgWDPlot": hourAvgWDPlot,
                       "hourAvgMonthPlot": hourAvgMonthPlot}

    for key, value in plotsDictionary.items():
        plotly.offline.plot(value, filename=(dir + r'\images\sites\{}.html'.format(key)))
        go.Figure(value).write_image(dir + r'\images\plots\{}.png'.format(key), width=1280, height=640)

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    graphs(project_dir)
    # main(project_dir)

