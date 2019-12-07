import pandas as pd
from pathlib import Path
import matplotlib

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
    WeatherData = pd.read_csv(dir + r'\data\processed\WeatherConditionsHourly2015.csv', delimiter=",", encoding="utf-8")

    RentalData = pd.DataFrame(RentalData.groupby(["DataHour", "Hour"])['Count'].sum()).reset_index()

    MergedData = pd.merge(left=RentalData, right=WeatherData, left_on="DataHour", right_on="Date", how='right')
    print(MergedData)

    MergedData.to_csv(dir + r'\data\processed\MergedData.csv', encoding='utf-8', index=False)
    RentalData.to_csv(dir + r'\data\processed\RentalDataMerged.csv', encoding='utf-8', index=False)

    return

def plots(dir):
    # Unpacking return variables from main function
    dockingStationsPlot = main(dir)

    tablesDictionary = {"dockingStationsPlot": dockingStationsPlot}

    for key, value in tablesDictionary.items():
        plotly.offline.plot(value, filename=(dir + r'\images\sites\{}.html'.format(key)))
        go.Figure(value).write_image(dir + r'\images\plots\{}.png'.format(key), width=1280)

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    plots(project_dir)

