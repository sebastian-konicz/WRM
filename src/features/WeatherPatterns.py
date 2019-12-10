import pandas as pd
from pathlib import Path
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np

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
    WeatherDataHour = pd.read_csv(dir + r'\data\processed\WeatherConditionsHourly2015.csv', delimiter=",", encoding="utf-8")
    WeatherDataDaily = pd.read_csv(dir + r'\data\processed\WeatherConditionsHourly2015.csv', delimiter=",",
                                  encoding="utf-8")

    RentalDataHour = pd.DataFrame(RentalData.groupby(["DataHour", "Hour"])['Count'].sum()).reset_index()
    RentalDataHour = pd.DataFrame(RentalData.groupby(["DataHour", "Hour"])['Count'].sum()).reset_index()

    # Merging dataframes
    MergedDataHour = pd.merge(left=RentalDataHour, right=WeatherDataHour, left_on="DataHour", right_on="Date", how='left')

    MergedDataHour = MergedDataHour.drop(columns=["Hour", "Unnamed: 0", "Date", "OnlyDate"])
    MergedDataHour.columns = ["DataHour", "count", "temp", "atemp", "precipitation",  "humidity",  "windspeed"]
    MergedDataHour = MergedDataHour[["DataHour", "temp", "atemp", "precipitation",  "humidity",  "windspeed", "count"]]
    print(MergedDataHour)

    corrMatrixHour = MergedDataHour[["temp", "atemp", "precipitation",  "humidity",  "windspeed", "count"]].corr()
    print(corrMatrixHour)

    mask = np.array(corrMatrixHour)
    mask[np.tril_indices_from(mask)] = False
    fig,ax = plt.subplots()
    fig.set_size_inches(10, 10)
    sn.heatmap(corrMatrixHour, mask=mask, vmin=-1, vmax=1, square=True, annot=True, linewidths=.5)
    plt.show()

    # MergedData.to_csv(dir + r'\data\processed\MergedData.csv', encoding='utf-8', index=False)

    return corrPlot

def plots(dir):
    # Unpacking return variables from main function
    corrPlot = main(dir)

    tablesDictionary = {"corrPlot": corrPlot}

    for key, value in tablesDictionary.items():
        plotly.offline.plot(value, filename=(dir + r'\images\sites\{}.html'.format(key)))
        go.Figure(value).write_image(dir + r'\images\plots\{}.png'.format(key), width=1280)

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    plots(project_dir)

