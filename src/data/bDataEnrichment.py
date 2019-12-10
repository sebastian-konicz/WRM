import pandas as pd
from pathlib import Path
import time

pd.options.display.max_columns = 50

def main(dir, dataYear):
    # Loading Data Set
    print("Loading dataset")
    RentalData = pd.read_csv(dir + r'\data\processed\RentalData2015.csv', delimiter=",", encoding="utf-8")

    # Setting the national holidays and changing list values to datetime objects
    NationalHolidays = ["2015-01-01", "2015-01-06", "2015-04-05", "2015-04-06", "2015-05-01", "2015-05-03",
                        "2015-05-24", "2015-06-04", "2015-08-15", "2015-11-01", "2015-11-11", "2015-12-25", "2015-12-26"]
    holidays = []
    for i in NationalHolidays:
        date = pd.to_datetime(i).date()
        holidays.append(date)

    # Creating datatime columns for analysis
    RentalData["StartDate"] = pd.to_datetime(RentalData["StartDate"])
    RentalData["EndDate"] = pd.to_datetime(RentalData["EndDate"])
    RentalData['Date'] = RentalData["StartDate"].map(lambda x: x.date())
    RentalData['Hour'] = RentalData["StartDate"].map(lambda x: x.hour)
    RentalData['Weekday'] = RentalData["StartDate"].map(lambda x: x.weekday())
    RentalData['Month'] = RentalData["StartDate"].map(lambda x: x.month)
    RentalData["Holiday"] = RentalData["Date"].isin(holidays)
    RentalData['Holiday'] = RentalData.apply(lambda RentalData: 1 if (RentalData["Holiday"] is True) else 0, axis=1)
    RentalData["WorkingDay"] = RentalData.apply(lambda RentalData: 1 if ((RentalData['Weekday'] >= 0) & (RentalData['Weekday'] < 5) & (RentalData['Holiday'] != 1)) else 0, axis=1)
    # RentalData["DateHour"] = RentalData.apply(lambda RentalData: RentalData["Date"].strftime('%Y-%m-%d') + " " + str(RentalData["Hour"]) + ":00:00", axis=1)
    RentalData["DateHour"] = RentalData.apply(lambda RentalData: RentalData["Date"].strftime('%Y-%m-%d') + " " + time.strftime('%H:%M:%S', (1, 1, 1, RentalData["Hour"], 0, 0, 0, 0, 0)), axis=1)

    # Changing numeric values to text values
    RentalData["Weekday"] = RentalData["Weekday"].map({0: "Monday", 1: "Tuesday", 2: "Wednesday",
                                                      3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"})
    RentalData["Month"] = RentalData["Month"].map({1: "January", 2: "February", 3: "March", 4: "April",
                                                   5: "May", 6: "June", 7: "July", 8: "August",
                                                   9: "September", 10: "October", 11: "November", 12: "December"})
    RentalData["WorkingDay"] = RentalData["WorkingDay"].map({0: "DayOff", 1: "WorkingDay"})


    # Changing values to category type
    categoryVariableList = ["Hour", "Weekday", "Month", "WorkingDay"]
    for var in categoryVariableList:
        RentalData[var] = RentalData[var].astype("category")

    # Adding technical column count
    RentalData['Count'] = 1

    print("Saving to Excel")
    RentalData.to_csv(dir + r'\data\processed\RentalData{}Enriched.csv'.format(dataYear), encoding='utf-8', index=False)

if __name__ == "__main__":
    # dataYear = input("Please chose year fo analysis (2015 or 2016) \n")
    dataYear = 2015
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir, dataYear)