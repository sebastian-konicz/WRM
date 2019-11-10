from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pandas as pd
import folium
from folium import plugins
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.colors import LinearSegmentedColormap, rgb_to_hsv, hsv_to_rgb
import scipy.ndimage.filters
import time
import datetime
import os.path
import io
import os
os.environ["PATH"] += os.pathsep + "."
from pathlib import Path
# %matplotlib inline

import ConsolidatedFunctions as cf

def main(dir):
    # Loading Data Set
    print("Loading dataset")
    RentalData = pd.read_csv(dir + r'\data\processed\RentalData2015.csv', delimiter=",", encoding="utf-8")

    # Changind the StartDate and EndDate to datetime format
    RentalData["StartDate"] = pd.to_datetime(RentalData["StartDate"])
    RentalData["EndDate"] = pd.to_datetime(RentalData["EndDate"])

    # Limiting dataset to weekdays
    RentalData['WeekDay'] = RentalData["StartDate"].dt.weekday
    RentalData = RentalData[(RentalData['WeekDay'] >= 0) & (RentalData['WeekDay'] < 5)]
    RentalData = RentalData.reset_index(drop=True)

    # Extracting hour of the day
    RentalData['hour_start'] = RentalData["StartDate"].map(lambda x: x.hour)
    RentalData['hour_end'] = RentalData["StartDate"].map(lambda x: x.hour)

    # Limiting the dataset to trips made between different stations
    RentalData = RentalData[RentalData['StartStation'] != RentalData['EndStation']]
    RentalData = RentalData.reset_index(drop=True)

    def interpolate(df1, df2, x):
        """return a weighted average of two dataframes"""
        df = df1 * (1 - x) + df2 * x
        return df.replace(np.nan, 0)

    def get_trip_counts_by_minute(float_hour, data):
        """get an interpolated dataframe for any time, based
        on hourly data"""

        columns = ["s_lat",
                   "s_lng",
                   "Departure Count",
                   "Arrival Count"]
        df1 = cf.get_trip_counts_by_hour(int(float_hour), data)
        df2 = cf.get_trip_counts_by_hour(int(float_hour) + 1, data)

        df = interpolate(df1.loc[:, columns],
                         df2.loc[:, columns],
                         float_hour % 1)

        df["StartStation"] = df1["StartStation"]
        return df

    # folium_map = cf.plot_station_counts(get_trip_counts_by_minute(10, RentalData), zoom_start=13)
    # folium_map.save(dir + r"\images\NetArivalDeparturesMinutes.html")

    def go_arrivals_frame(i, hour_of_day, save_path):
        # create the map object
        data = get_trip_counts_by_minute(hour_of_day, RentalData)
        my_frame = cf.plot_station_counts(data, zoom_start=13)

        # generate the png file as a byte array
        png = my_frame._to_png()

        # now add a caption to the image to indicate the time-of-day.
        hour = int(hour_of_day)
        minutes = int((hour_of_day % 1) * 60)

        # create a PIL image object
        image = Image.open(io.BytesIO(png))
        draw = ImageDraw.ImageDraw(image)

        # load a font
        font = ImageFont.truetype("arial.ttf", 30)

        # draw time of day text
        draw.text((20, image.height - 50),
                  "time: {:0>2}:{:0>2}h".format(hour, minutes),
                  fill=(255, 255, 255),
                  font=font)

        # draw title
        draw.text((image.width - 400, 20),
                  "Net Arrivals vs Time of Day",
                  fill=(255, 255, 255),
                  font=font)

        # write to a png file
        filename = os.path.join(save_path, "frame_{:0>5}.png".format(i))
        image.save(filename, "PNG")
        return image

    print("Writing pictures for")
    dir_name = dir + r'\images\final\AIM'
    arrival_times = np.arange(5, 23, .2)
    for i, hour in enumerate(arrival_times):
        print("making image for " + str(i) + " " + str(hour))
        go_arrivals_frame(i, hour, dir_name)

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir)
