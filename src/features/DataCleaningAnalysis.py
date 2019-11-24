import pandas as pd
from pathlib import Path
import geopy.distance as gd

pd.options.display.max_columns = 50

def main(dir, dataYear):
    # LOADING DATA FROM DIRECTORY
    dataPath = dir + r'\data\interim'
    print("Loading Datasets")
    # Rental dataset
    RentalData = pd.read_excel(dataPath + r'\RentalData{}.xlsx'.format(dataYear))

    # Getting the number of rows
    print(RentalData.index.max())
    datasetBeforeCleaning = RentalData.index.max()

    # Docking station dataset
    DockingStations = pd.read_excel(dataPath + r'\DockingStationsHistorical.xlsx')

    # Merging Rental dataset with Dockin Stations dataset to get geocoordinates of stations
    print("Merging datasets")
    # Adding geolocation to start station
    RentalData = pd.merge(left=RentalData, right=DockingStations[['number', 'lat', 'lng', 'name', 'name_old']],
                             left_on="Stacja wynajmu", right_on="name_old", how='left')
    # Adding geolocation to endstation station
    RentalData = pd.merge(left=RentalData, right=DockingStations[['number', 'lat', 'lng', 'name', 'name_old']], suffixes=("", "_e"),
                             left_on="Stacja zwrotu", right_on="name_old", how='left')

    # Getting the number of rows
    RentalData = RentalData.reset_index(drop=True)
    print(RentalData.index.max())
    datasetAfterMerging = RentalData.index.max()

    # Renaming columns
    RentalData.columns = ["Lp", "BikeNumber", "StartDate", "EndDate", "StartStation_old", "EndStation_old",
                          's_number', "s_lat", "s_lng", 'StartStation', 's_name_old',
                          'e_number', 'e_lat', 'e_lng', 'EndStation', 'e_name_old']

    # Adding technical column count
    RentalData['Count'] = 1

    # Limiting datasets to valid rides i.e excluding rides made between the same station and shorter than 5 minutes
    print("Limiting data set to valid rides")
    RentalData["StartDate"] = pd.to_datetime(RentalData["StartDate"])
    RentalData["EndDate"] = pd.to_datetime(RentalData["EndDate"])
    RentalData['Duration'] = RentalData.apply(lambda RentalData: RentalData['EndDate'] - RentalData['StartDate'], axis=1)
    RentalData['Duration'] = RentalData.apply(lambda RentalData: int(RentalData['Duration'].total_seconds()), axis=1)
    RentalData['Date'] = RentalData["StartDate"].map(lambda x: x.date())

    # All rentals analysys
    AllRental = pd.DataFrame(RentalData.groupby(["Date", "BikeNumber"], sort=True)["Count"].count()).reset_index()
    AllRental = pd.DataFrame(AllRental.groupby(["BikeNumber"], sort=True)["Count"].mean()).reset_index()
    AllRental["Count"] = AllRental.apply(lambda AllRental: round(int(AllRental["Count"]), 2), axis=1)
    AllRental.to_csv(dir + r'\data\interim\AllRental{}.csv'.format(dataYear), encoding='utf-8', index=False)

    ShortRental = RentalData[(RentalData['StartStation'] == RentalData['EndStation']) & (RentalData['Duration'] < 300)]
    RentalData = RentalData.drop(RentalData[(RentalData['StartStation'] == RentalData['EndStation']) & (RentalData['Duration'] < 300)].index)

    # Getting the number of rows
    RentalData = RentalData.reset_index(drop=True)
    print(RentalData.index.max())
    datasetAfterMerging = RentalData.index.max()

    # Long rental analysys
    LongRental = pd.DataFrame(RentalData.groupby(["Date", "BikeNumber"], sort=True)["Count"].count()).reset_index()
    LongRental = pd.DataFrame(LongRental.groupby(["BikeNumber"], sort=True)["Count"].mean()).reset_index()
    LongRental["Count"] = LongRental.apply(lambda LongRental: round(int(LongRental["Count"]), 2), axis=1)
    LongRental.to_csv(dir + r'\data\interim\LongRental{}.csv'.format(dataYear), encoding='utf-8', index=False)

    # Short rental analysys
    ShortRental = pd.DataFrame(ShortRental.groupby(["Date", "BikeNumber"], sort=True)["Count"].count()).reset_index()
    print("Saving to Excel")
    ShortRental.to_csv(dir + r'\data\interim\ShortRental1{}.csv'.format(dataYear), encoding='utf-8', index=False)
    ShortRental = pd.DataFrame(ShortRental.groupby(["BikeNumber"], sort=True)["Count"].mean()).reset_index()
    ShortRental["Count"] = ShortRental.apply(lambda ShortRental: round(int(ShortRental["Count"]), 2), axis=1)
    print(ShortRental.tail())
    print("Saving to Excel")
    ShortRental.to_csv(dir + r'\data\interim\ShortRental2{}.csv'.format(dataYear), encoding='utf-8', index=False)

    # Mean rental number
    MeanRentalNumbeLAll = AllRental["Count"].mean()
    MeanRentalNumbeLong = LongRental["Count"].mean()
    MeanRentalNumbeShort = ShortRental["Count"].mean()
    print("MeanRentalNumberAll = " + str(MeanRentalNumbeLAll))
    print("MeanRentalNumbeLong = " + str(MeanRentalNumbeLong))
    print("MeanRentalNumbeShort = " + str(MeanRentalNumbeShort))

    RentalData = RentalData.reset_index(drop=True)
    print(RentalData.index.max())

    # Limiting dataset to rides longer than 0 seconds (negative values are present due to time change on 2015-10-25)
    print("Limiting dataset to rides longer than 0 seconds")
    RentalData = RentalData[RentalData['Duration'] > 0]
    RentalData = RentalData.reset_index(drop=True)
    print(RentalData.index.max())

    # Limiting dataset to rentals from docking stations and to docking staions
    print("Limiting dataset to rentals from docking stations and to docking staions")
    RentalData = RentalData[RentalData['s_lat'] > 0]
    RentalData = RentalData[RentalData['e_lat'] > 0]
    RentalData = RentalData.reset_index(drop=True)
    print(RentalData.index.max())

    # Calculating distance and speed
    print("Calculating distance and speed")
    RentalData['Distance'] = RentalData.apply(lambda RentalData: round(int(gd.distance((RentalData['s_lat'], RentalData['s_lng']), (RentalData['e_lat'], RentalData['e_lng'])).km), 3), axis=1)
    RentalData['Speed'] = RentalData.apply(lambda RentalData: round(int((RentalData['Distance']/RentalData['Duration'])* 3600), 2), axis=1)

    # Limiting dataset to rentals with speed less than
    print("Limiting dataset to rentals with speed less than ")


    # Limiting dataset
    RentalData = RentalData[["BikeNumber", "StartDate", "EndDate", "Duration", "Distance", "Speed",
                             "StartStation", 's_number', "s_lat", "s_lng",
                             "EndStation", 'e_number', 'e_lat', 'e_lng', "Count"]]

    # Sorting values by rental id = by date
    RentalData.sort_values(by="StartDate", ascending=True, inplace=True)

    # Reseting index
    RentalData = RentalData.reset_index(drop=True)

    # print("Saving to Excel")
    # RentalData.to_csv(dir + r'\data\processed\RentalData{}.csv'.format(dataYear), encoding='utf-8', index=False)

if __name__ == "__main__":
    dataYear = input("Please chose year fo analysis (2015 or 2016) \n")
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir, dataYear)