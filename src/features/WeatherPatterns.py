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
    WeatherDataDaily = pd.read_csv(dir + r'\data\processed\WeatherConditionsDaily2015.csv', delimiter=",", encoding="utf-8")

    RentalDataHour = pd.DataFrame(RentalData.groupby(["DateHour", "Hour"])['Count'].sum()).reset_index()
    RentalDataDaily = pd.DataFrame(RentalData.groupby(["Date"])['Count'].sum()).reset_index()

    # Merging dataframes - hourly
    MergedDataHour = pd.merge(left=RentalDataHour, right=WeatherDataHour, left_on="DateHour", right_on="Date", how='left')

    # Reshaping merged dataframe - hourly
    MergedDataHour = MergedDataHour.drop(columns=["Hour", "Unnamed: 0", "Date", "OnlyDate"])
    MergedDataHour.columns = ["dateHour", "count", "temp", "atemp", "precipitation",  "humidity",  "windspeed"]
    MergedDataHour["humidity"] = MergedDataHour.apply(lambda MergedDataHour: MergedDataHour["humidity"] * 100, axis=1)
    MergedDataHour = MergedDataHour[["dateHour", "temp", "atemp", "precipitation",  "humidity",  "windspeed", "count"]]

    # Merging dataframes - daily
    MergedDataDaily = pd.merge(left=RentalDataDaily, right=WeatherDataDaily, left_on="Date", right_on="Date", how='left')

    # Reshaping merged dataframe - daily
    MergedDataDaily = MergedDataDaily.drop(columns="Unnamed: 0")
    MergedDataDaily.columns = ["date", "count", "tempMin", "tempMax", "atempMin", "atempMax", "precipitation",  "humidity",  "windspeed", "visipbility"]
    MergedDataDaily = MergedDataDaily[["date", "tempMax", "atempMax", "precipitation",  "humidity",  "windspeed", "count"]]


    # ploting correlation - weather hourly
    corrMatrixHour = MergedDataHour[["temp", "atemp", "precipitation",  "humidity",  "windspeed", "count"]].corr()

    mask = np.array(corrMatrixHour)
    mask[np.tril_indices_from(mask)] = False
    figHour, ax = plt.subplots()
    plt.title("Coreelation heatmap")
    figHour.set_size_inches(10, 10)
    heatmapDaily = sn.heatmap(corrMatrixHour, mask=mask, vmin=-1, vmax=1, square=True, annot=True, linewidths=.5)
    heatmapDaily = heatmapDaily.get_figure()

    # # Regression plots
    # figReg, (ax1, ax2, ax3) = plt.subplots(ncols=3)
    # figReg.set_size_inches(20, 5)
    # sn.regplot(x="temp", y="count", data=MergedDataHour, ax=ax1)
    # sn.regplot(x="windspeed", y="count", data=MergedDataHour, ax=ax2)
    # sn.regplot(x="humidity", y="count", data=MergedDataHour, ax=ax3)
    # plt.show()

    figCorrTemp, ax1 = plt.subplots()
    figCorrTemp.set_size_inches(12.8, 6.4)
    plt.title("Coreelation between temperature and count of trips")
    plotCorrTemp = sn.regplot(x="temp", y="count", data=MergedDataHour, ax=ax1, color="g")
    plotCorrTemp = plotCorrTemp.get_figure()

    figCorrHum, ax1 = plt.subplots()
    figCorrHum.set_size_inches(12.8, 6.4)
    plt.title("Coreelation between humidity and count of trips")
    plotCorrHum = sn.regplot(x="humidity", y="count", data=MergedDataHour, ax=ax1, color="y")
    plotCorrHum = plotCorrHum.get_figure()

    figCorrWind, ax1 = plt.subplots()
    figCorrWind.set_size_inches(12.8, 6.4)
    plt.title("Coreelation between windspeed and count of trips")
    plotCorrWind = sn.regplot(x="windspeed", y="count", data=MergedDataHour, ax=ax1)
    plotCorrWind = plotCorrWind.get_figure()

    plt.show()

    # MergedData.to_csv(dir + r'\data\processed\MergedData.csv', encoding='utf-8', index=False)

    return heatmapDaily, plotCorrTemp, plotCorrHum, plotCorrWind

def plots(dir):
    # Unpacking return variables from main function
    heatmapDaily, plotCorrTemp, plotCorrHum, plotCorrWind = main(dir)

    tablesDictionary = {"heatmapDaily": heatmapDaily, "plotCorrTemp": plotCorrTemp, "plotCorrHum": plotCorrHum,
                        "plotCorrWind": plotCorrWind}

    for key, value in tablesDictionary.items():
        value.savefig(dir + r'\images\plots\{}.png'.format(key))

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    plots(project_dir)

