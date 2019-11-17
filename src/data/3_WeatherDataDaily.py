import pandas as pd
from pathlib import Path
import requests
import datetime
import time
from functools import reduce
import json

def main(dir, dataYear):
        # Loading data
        print("Loading data")
        RentalData = pd.read_csv(dir + r'\data\processed\RentalData{}.csv'.format(dataYear))

        # Getting unique dates form dataframe
        RentalData["StartDate"] = pd.to_datetime(RentalData["StartDate"])
        RentalData['Date'] = RentalData["StartDate"].map(lambda x: x.date())
        RentalData = RentalData[["Date", "StartDate"]]
        Dates = RentalData.groupby("Date").first()

        APIKEY = "3c7e3a27611cb8f6c1812270bcf762b9"

        weather = []
        for index, row in Dates.iterrows():
            # Getting UNIX timestamp
            date = pd.to_datetime(row["StartDate"]).date()
            print(date)
            unixtime = round(time.mktime(date.timetuple())) + 7200 # Added 10800 to set correct time zone and time to 1 AM
            print(unixtime)

            # Getting API response for given date
            url = "https://api.darksky.net/forecast/{}/51.0983,17.0261,{}?lang=pl&units=si&exclude=currently,flags".format(APIKEY, unixtime)
            JSONdata = requests.get(url).json()

            # Getting relevant data and appending the weather list
            if 'error' not in JSONdata:
                weather.append([date,
                               JSONdata['daily']['data'][0]['temperatureMin'],
                               JSONdata['daily']['data'][0]['temperatureMax'],
                               JSONdata['daily']['data'][0]['apparentTemperatureMin'],
                               JSONdata['daily']['data'][0]['apparentTemperatureMax'],
                               JSONdata['daily']['data'][0]['precipIntensity'],
                               JSONdata['daily']['data'][0]['humidity'],
                               JSONdata['daily']['data'][0]['windSpeed'],
                               JSONdata['daily']['data'][0]['visibility']])

        weatherConditions = pd.DataFrame(weather)
        weatherConditions.columns = ['Date', 'temperatureMin', 'temperatureMax', 'apparentTemperatureMin',
                                     'apparentTemperatureMax', 'precipIntensity', 'humidity', 'windSpeed', 'visibility']

        weatherConditions.to_csv(dir + r'\data\processed\WeatherConditionsDaily{}.csv'.format(dataYear))

if __name__ == "__main__":
    dataYear = input("Please chose year fo analysis (2015 or 2016) \n")
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir, dataYear)