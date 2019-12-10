import pandas as pd
from pathlib import Path
import requests
from datetime import datetime
import time

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

        timechange = "2015-10-26"
        timechange = pd.to_datetime(timechange).date()
        print(timechange)

        weatherHourly = []
        for index, row in Dates.iterrows():
            # Getting UNIX timestamp
            date = pd.to_datetime(row["StartDate"]).date()
            print(date)
            if date >= timechange:
                unixtime = round(time.mktime(date.timetuple())) + 3600  # Added 10800 to set correct time zone and time to 1 AM
                print("after time change")
            else:
                unixtime = round(time.mktime(date.timetuple())) + 7200 # Added 10800 to set correct time zone and time to 1 AM
                print("before time change")
            print(unixtime)

            # Getting API response for given date
            url = "https://api.darksky.net/forecast/{}/51.0983,17.0261,{}?lang=pl&units=si&exclude=currently,flags".format(APIKEY, unixtime)
            JSONdata = requests.get(url).json()

            weather = []
            for i in range(0, 24):
                # Getting relevant data and time and appending the weather list
                if 'error' not in JSONdata:
                    if date >= timechange:
                        timestamp = int(JSONdata['hourly']['data'][i]['time']) + 3600
                    else:
                        timestamp = int(JSONdata['hourly']['data'][i]['time']) + 7200
                    timeDate = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
                    weather.append([timeDate,
                                   JSONdata['hourly']['data'][i]['temperature'],
                                   JSONdata['hourly']['data'][i]['apparentTemperature'],
                                   JSONdata['hourly']['data'][i]['precipIntensity'],
                                   JSONdata['hourly']['data'][i]['humidity'],
                                   JSONdata['hourly']['data'][i]['windSpeed']])

            # creating dataframe for specific date
            weatherConditions = pd.DataFrame(weather)
            weatherConditions.columns = ['Date', 'temperature', 'apparentTemperature',
                                         'precipIntensity', 'humidity', 'windSpeed']
            weatherHourly.append(weatherConditions)

        weatherHourlyConditions = pd.concat(weatherHourly)
        weatherHourlyConditions = weatherHourlyConditions.reset_index(drop=True)
        print(weatherHourlyConditions)

        weatherHourlyConditions["Date"] = pd.to_datetime(weatherHourlyConditions["Date"])
        weatherHourlyConditions['OnlyDate'] = weatherHourlyConditions["Date"].map(lambda x: x.date())
        grouped = weatherHourlyConditions.groupby('OnlyDate')['temperature'].mean()
        print(grouped)

        weatherHourlyConditions.to_csv(dir + r'\data\processed\WeatherConditionsHourly{}.csv'.format(dataYear), header=True)
        grouped.to_csv(dir + r'\data\processed\WeatherConditionsMeanTemperature{}.csv'.format(dataYear), header=True)

if __name__ == "__main__":
    dataYear = input("Please chose year fo analysis (2015 or 2016) \n")
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir, dataYear)