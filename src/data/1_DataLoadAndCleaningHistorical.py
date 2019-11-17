import pandas as pd
from pathlib import Path

pd.options.display.max_columns = 50

def main(dir, dataYear):
    # LOADING DATA FROM DIRECTORY
    dataPath = dir + r'\data\interim'
    print("Loading Datasets")
    # Rental dataset
    RentalData = pd.read_excel(dataPath + r'\RentalData{}.xlsx'.format(dataYear))
    print(RentalData.tail())
    print(RentalData.index.max())

    # Docking station dataset
    DockingStations = pd.read_excel(dataPath + r'\DockingStationsHistorical.xlsx')

    # Dropping duplicate values

    # Merging Rental dataset with Dockin Stations dataset to get geocoordinates of stations
    # Adding geolocation to start station
    RentalData = pd.merge(left=RentalData, right=DockingStations[['number', 'lat', 'lng', 'name', 'name_old']],
                             left_on="Stacja wynajmu", right_on="name_old", how='left')
    # Adding geolocation to endstation station
    RentalData = pd.merge(left=RentalData, right=DockingStations[['number', 'lat', 'lng', 'name', 'name_old']], suffixes=("", "_e"),
                             left_on="Stacja zwrotu", right_on="name_old", how='left')

    RentalData = RentalData.reset_index(drop=True)
    print(RentalData.tail())
    print(RentalData.index.max())

    # Renaming columns
    RentalData.columns = ["Lp", "BikeNumber", "StartDate", "EndDate", "StartStation_old", "EndStation_old",
                          's_number', "s_lat", "s_lng", 'StartStation', 's_name_old',
                          'e_number', 'e_lat', 'e_lng', 'EndStation', 'e_name_old']

    # Limiting data sets to valid rides i.e excluding rides made between the same station and shorter than 5 minutes
    RentalData["StartDate"] = pd.to_datetime(RentalData["StartDate"])
    RentalData["EndDate"] = pd.to_datetime(RentalData["EndDate"])
    RentalData['Duration'] = RentalData.apply(lambda RentalData: RentalData['EndDate'] - RentalData['StartDate'], axis=1)
    RentalData['Duration'] = RentalData.apply(lambda RentalData: int(RentalData['Duration'].total_seconds()), axis=1)
    RentalData = RentalData.drop(RentalData[(RentalData['StartStation'] == RentalData['EndStation']) & (RentalData['Duration'] < 300)].index)
    RentalData = RentalData.reset_index(drop=True)
    print(RentalData.tail())
    print(RentalData.index.max())

    # Limiting data set to rides longer than 0 seconds (negative values are present due to time change on 2015-10-25)
    RentalData = RentalData[RentalData['Duration'] > 0]
    RentalData = RentalData.reset_index(drop=True)
    print(RentalData.tail())
    print(RentalData.index.max())

    # Limiting dataset
    RentalData = RentalData[["BikeNumber", "StartDate", "EndDate", "Duration",
                             "StartStation", 's_number', "s_lat", "s_lng",
                             "EndStation", 'e_number', 'e_lat', 'e_lng']]

    # Sorting values by rental id = by date
    RentalData.sort_values(by="StartDate", ascending=True, inplace=True)

    # Limiting dataset to rentals from docking stations and to docking staions
    RentalData = RentalData[RentalData['s_lat'] > 0]
    RentalData = RentalData[RentalData['e_lat'] > 0]

    # Reseting index
    RentalData = RentalData.reset_index(drop=True)

    print("Saving to Excel")
    RentalData.to_csv(dir + r'\data\processed\RentalData{}.csv'.format(dataYear), encoding='utf-8', index=False)

if __name__ == "__main__":
    dataYear = input("Please chose year fo analysis (2015 or 2016) \n")
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir, dataYear)