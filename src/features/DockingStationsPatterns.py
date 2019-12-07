import pandas as pd
from pathlib import Path

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

    outflow = RentalData[["StartStation", "Count"]]
    outflow = pd.DataFrame(outflow.groupby("StartStation")['Count'].sum()).reset_index()
    outflow.sort_values(by="Count", ascending=False, inplace=True)
    outflow.columns = ["Station", "Outflow"]

    inflow = RentalData[["EndStation", "Count"]]
    inflow = pd.DataFrame(inflow.groupby("EndStation")['Count'].sum()).reset_index()
    inflow.sort_values(by="Count", ascending=False, inplace=True)
    inflow.columns = ["Station", "Inflow"]

    totalFlow = pd.merge(left=outflow, right=inflow, left_on="Station", right_on="Station", how='left')
    totalFlow["TotalFlows"] = totalFlow.apply(lambda totalFlow: totalFlow['Outflow'] + totalFlow['Inflow'], axis=1)
    totalFlow.sort_values(by="TotalFlows", ascending=False, inplace=True)

    flowDiff = totalFlow.copy()
    flowDiff["InflowsOutflows"] = flowDiff.apply(lambda totalFlow: totalFlow['Outflow'] - totalFlow['Inflow'], axis=1)
    flowDiff.sort_values(by="InflowsOutflows", ascending=True, inplace=True)

    rankData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    rank = pd.DataFrame(rankData, columns=["Rank"])

    # REstring data to top 10 values
    outflow = outflow.head(10)
    inflow = inflow.head(10)
    totalFlow = totalFlow.head(10)
    flowDiff = flowDiff.head(10)

    # Creating tables
    headerColor = 'black'
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    outflowTable = go.Figure(data=[go.Table(
        columnwidth=[2, 30, 10],
        header=dict(
            values=['<b>Rank</b>', '<b>Station</b>', '<b>Outflow</b>'],
            line_color='black',
            fill_color=headerColor,
            align=['center'],
            font=dict(color='white', size=14),
            height=30
        ),
        cells=dict(
            values=[rank.Rank, outflow.Station, outflow.Outflow],
            line_color='darkslategray',
            fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor] * 3],
            align=['left', 'left', 'center'],
            font=dict(color='black', size=14),
            height=25
        ))
    ])

    inflowTable = go.Figure(data=[go.Table(
        columnwidth=[2, 30, 10],
        header=dict(
            values=['<b>Rank</b>', '<b>Station</b>', '<b>Inflow</b>'],
            line_color='black',
            fill_color=headerColor,
            align=['center'],
            font=dict(color='white', size=14),
            height=30
        ),
        cells=dict(
            values=[rank.Rank, inflow.Station, inflow.Inflow],
            line_color='darkslategray',
            fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor] * 3],
            align=['left', 'left', 'center'],
            font=dict(color='black', size=14),
            height=25
        ))
    ])

    totalflowTable = go.Figure(data=[go.Table(
        columnwidth=[2, 30, 10],
        header=dict(
            values=['<b>Rank</b>', '<b>Station</b>', '<b>Total Flows</b>'],
            line_color='black',
            fill_color=headerColor,
            align=['center'],
            font=dict(color='white', size=14),
            height=30
        ),
        cells=dict(
            values=[rank.Rank, totalFlow.Station, totalFlow.TotalFlows],
            line_color='darkslategray',
            fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor] * 3],
            align=['left', 'left', 'center'],
            font=dict(color='black', size=14),
            height=25
        ))
    ])

    flowDiffTable = go.Figure(data=[go.Table(
        columnwidth=[2, 30, 10],
        header=dict(
            values=['<b>Rank</b>', '<b>Station</b>', '<b>Inflows - Outflows</b>'],
            line_color='black',
            fill_color=headerColor,
            align=['center'],
            font=dict(color='white', size=14),
            height=30
        ),
        cells=dict(
            values=[rank.Rank, flowDiff.Station, flowDiff.InflowsOutflows],
            line_color='darkslategray',
            fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor] * 3],
            align=['left', 'left', 'center'],
            font=dict(color='black', size=14),
            height=25
        ))
    ])

    # Creating pie chart
    # Total chart
    dockingStationsSame = RentalData[RentalData['StartStation'] == RentalData['EndStation']]
    dockingStationsSame = pd.DataFrame(dockingStationsSame.groupby("StartStation")['Count'].sum()).reset_index()
    dockingStationsSame = dockingStationsSame['Count'].sum()
    print(dockingStationsSame)

    dockingStationsDiff = RentalData[RentalData['StartStation'] != RentalData['EndStation']]
    dockingStationsDiff = pd.DataFrame(dockingStationsDiff.groupby("StartStation")['Count'].sum()).reset_index()
    dockingStationsDiff = dockingStationsDiff['Count'].sum()
    print(dockingStationsDiff)

    dockingStationsLabels = ['Same Station', 'Different Station']
    dockingStationsValues = [dockingStationsSame, dockingStationsDiff]

    dockingStationsPlotData = go.Pie(labels=dockingStationsLabels, values=dockingStationsValues, pull=[0, 0.2])

    dockingStationsPlotLayout = go.Layout(template="plotly_dark", title=go.layout.Title(text="Total no. of rentals", x=0.5, y=0.95, xanchor='center', yanchor='middle'))

    dockingStationsPlot = dict(data=dockingStationsPlotData, layout=dockingStationsPlotLayout)

    # Day off chart
    dockingStationsDO = RentalData[RentalData["WorkingDay"] == "DayOff"]

    dockingStationsDOSame = dockingStationsDO[dockingStationsDO['StartStation'] == dockingStationsDO['EndStation']]
    dockingStationsDOSame = pd.DataFrame(dockingStationsDOSame.groupby("StartStation")['Count'].sum()).reset_index()
    dockingStationsDOSame = dockingStationsDOSame['Count'].sum()
    print(dockingStationsDOSame)

    dockingStationsDODiff = dockingStationsDO[dockingStationsDO['StartStation'] != dockingStationsDO['EndStation']]
    dockingStationsDODiff = pd.DataFrame(dockingStationsDODiff.groupby("StartStation")['Count'].sum()).reset_index()
    dockingStationsDODiff = dockingStationsDODiff['Count'].sum()
    print(dockingStationsDODiff)

    dockingStationsDOLabels = ['Same Station', 'Different Station']
    dockingStationsDOValues = [dockingStationsDOSame, dockingStationsDODiff]

    dockingStationsDOPlot = go.Pie(labels=dockingStationsDOLabels, values=dockingStationsDOValues, pull=[0, 0.2])

    # Working Day chart
    dockingStationsWD = RentalData[RentalData["WorkingDay"] == "WorkingDay"]

    dockingStationsWDSame = dockingStationsWD[dockingStationsWD['StartStation'] == dockingStationsWD['EndStation']]
    dockingStationsWDSame = pd.DataFrame(dockingStationsWDSame.groupby("StartStation")['Count'].sum()).reset_index()
    dockingStationsWDSame = dockingStationsWDSame['Count'].sum()
    print(dockingStationsWDSame)

    dockingStationsWDDiff = dockingStationsWD[dockingStationsWD['StartStation'] != dockingStationsWD['EndStation']]
    dockingStationsWDDiff = pd.DataFrame(dockingStationsWDDiff.groupby("StartStation")['Count'].sum()).reset_index()
    dockingStationsWDDiff = dockingStationsWDDiff['Count'].sum()
    print(dockingStationsWDDiff)

    dockingStationsWDLabels = ['Same Station', 'Different Station']
    dockingStationsWDValues = [dockingStationsWDSame, dockingStationsWDDiff]

    dockingStationsWDPlot = go.Pie(labels=dockingStationsWDLabels, values=dockingStationsWDValues, pull=[0, 0.2])

    # Creating subplots duration on working days / days off
    dockingStationsWDDOPlot = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]], subplot_titles=("week days", "days off"))

    dockingStationsWDDOPlot.add_trace(dockingStationsWDPlot, 1, 1)
    dockingStationsWDDOPlot.add_trace(dockingStationsDOPlot, 1, 2)

    dockingStationsWDDOPlotLayout = go.Layout(template="plotly_dark",
                                          title=go.layout.Title(text="Types of trips (same station / differen station)", x=0.5, y=0.95,
                                                                xanchor='center', yanchor='middle'))
    dockingStationsWDDOPlot.update_layout(dockingStationsWDDOPlotLayout)

    return outflowTable, inflowTable, totalflowTable, flowDiffTable, dockingStationsWDDOPlot, dockingStationsPlot

def plots(dir):
    # Unpacking return variables from main function
    outflowTable, inflowTable, totalflowTable, flowDiffTable, dockingStationsWDDOPlot, dockingStationsPlot = main(dir)

    tablesDictionary = {"outflowTable": outflowTable, "inflowTable": inflowTable,
                        "totalflowTable": totalflowTable, "flowDiffTable": flowDiffTable,
                        "dockingStationsWDDOPlot": dockingStationsWDDOPlot, "dockingStationsPlot": dockingStationsPlot}

    for key, value in tablesDictionary.items():
        plotly.offline.plot(value, filename=(dir + r'\images\sites\{}.html'.format(key)))
        go.Figure(value).write_image(dir + r'\images\plots\{}.png'.format(key), width=1280)

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    plots(project_dir)
    # main(project_dir)

