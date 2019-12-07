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

    return outflowTable, inflowTable, totalflowTable, flowDiffTable

def plots(dir):
    # Unpacking return variables from main function
    outflowTable, inflowTable, totalflowTable, flowDiffTable = main(dir)

    tablesDictionary = {"outflowTable": outflowTable, "inflowTable": inflowTable,
                        "totalflowTable": totalflowTable, "flowDiffTable": flowDiffTable}

    for key, value in tablesDictionary.items():
        plotly.offline.plot(value, filename=(dir + r'\images\sites\{}.html'.format(key)))
        go.Figure(value).write_image(dir + r'\images\plots\{}.png'.format(key), width=1280)

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    plots(project_dir)
    # main(project_dir)

