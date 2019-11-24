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
    print(RentalData.index.max())

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
    RentalData = RentalData.reset_index(drop=True)
    print("Po mergu")
    print(RentalData.index.max())

    # Renaming columns
    RentalData.columns = ["Lp", "BikeNumber", "StartDate", "EndDate", "StartStation_old", "EndStation_old",
                          's_number', "s_lat", "s_lng", 'StartStation', 's_name_old',
                          'e_number', 'e_lat', 'e_lng', 'EndStation', 'e_name_old']

    # Limiting dataset to rentals from docking stations and to docking staions
    print("Limiting dataset to rentals from docking stations and to docking staions")
    RentalData = RentalData[RentalData['s_lat'] > 0]
    RentalData = RentalData[RentalData['e_lat'] > 0]
    RentalData = RentalData.reset_index(drop=True)
    print("Po limicie geolokalizacyjnym")
    print(RentalData.index.max())

    # Adding technical column count
    RentalData['Count'] = 1

    # Limiting datasets to valid rides i.e excluding rides made between the same station and shorter than 5 minutes
    print("Limiting data set to valid rides")
    RentalData["StartDate"] = pd.to_datetime(RentalData["StartDate"])
    RentalData["EndDate"] = pd.to_datetime(RentalData["EndDate"])
    RentalData['Duration'] = RentalData.apply(lambda RentalData: RentalData['EndDate'] - RentalData['StartDate'], axis=1)
    RentalData['Duration'] = RentalData.apply(lambda RentalData: int(RentalData['Duration'].total_seconds()), axis=1)
    RentalData = RentalData.drop(RentalData[(RentalData['StartStation'] == RentalData['EndStation']) & (RentalData['Duration'] < 300)].index)

    RentalData = RentalData.reset_index(drop=True)
    print("Po limicie czasowym")
    print(RentalData.index.max())

    # Limiting dataset to rides longer than 0 seconds (negative values are present due to time change on 2015-10-25)
    print("Limiting dataset to rides longer than 0 seconds")
    RentalData = RentalData[RentalData['Duration'] > 0]
    RentalData = RentalData.reset_index(drop=True)
    print("Po limicie czasowym >0")
    print(RentalData.index.max())

    # Calculating distance and speed
    print("Calculating distance and speed")
    RentalData['Distance'] = RentalData.apply(lambda RentalData: int(gd.distance((RentalData['s_lat'], RentalData['s_lng']), (RentalData['e_lat'], RentalData['e_lng'])).km), axis=1)
    RentalData['Speed'] = RentalData.apply(lambda RentalData: int((RentalData['Distance']/RentalData['Duration']) * 3600), axis=1)
    # Rounding values
    print("Rounding values")
    RentalData['Distance'] = RentalData.applymap(lambda RentalData: round(RentalData['Distance'], 3))
    RentalData['Speed'] = RentalData.applymap(lambda RentalData: round(RentalData['Speed'], 2))

    # Limiting dataset to rentals with speed less than 25
    print("Limiting dataset to rentals with speed less than 25")
    RentalData = RentalData.drop(RentalData[RentalData['Speed'] > 25].index)
    RentalData = RentalData.reset_index(drop=True)
    print("Po limicie prędkościowym max")
    print(RentalData.index.max())

    # Limiting dataset
    RentalData = RentalData[["BikeNumber", "StartDate", "EndDate", "Duration", "Distance", "Speed",
                             "StartStation", 's_number', "s_lat", "s_lng",
                             "EndStation", 'e_number', 'e_lat', 'e_lng', "Count"]]

    # Sorting values by rental id = by date
    RentalData.sort_values(by="StartDate", ascending=True, inplace=True)

    # Reseting index
    RentalData = RentalData.reset_index(drop=True)

    print("Saving to Excel")
    RentalData.to_csv(dir + r'\data\processed\RentalData{}.csv'.format(dataYear), encoding='utf-8', index=False)

if __name__ == "__main__":
    # dataYear = input("Please chose year fo analysis (2015 or 2016) \n")
    dataYear = 2015
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir, dataYear)