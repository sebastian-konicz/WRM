import pandas as pd
from pathlib import Path

pd.options.display.max_columns = 50

def main(dir, dataYear):
    # LOADING DATA FROM DIRECTORY
    dataPath = dir + r'\data\interim'
    print("Loading Datasets")

    # Rental dataset
    RentalData = pd.read_excel(dataPath + r'\RentalData{}.xlsx'.format(dataYear))

    # Docking station dataset
    DockingStations = pd.read_excel(dataPath + r'\DockingStationsHistorical.xlsx')

    # Dropping duplicate values

    print("Merging and cleaning data ")
    # Merging Rental dataset with Dockin Stations dataset to get geocoordinates of stations
    # Adding geolocation to start station
    RentalData = pd.merge(left=RentalData, right=DockingStations[['number', 'lat', 'lng', 'name', 'name_old']],
                             left_on="Stacja wynajmu", right_on="name_old", how='left')
    # Adding geolocation to endstation station
    RentalData = pd.merge(left=RentalData, right=DockingStations[['number', 'lat', 'lng', 'name', 'name_old']], suffixes=("", "_e"),
                             left_on="Stacja zwrotu", right_on="name_old", how='left')

    # Renaming columns
    RentalData.columns = ["Lp", "BikeNumber", "StartDate", "EndDate", "StartStation", "EndStation",
                          's_number', "s_lat", "s_lng", 's_name', 's_name_old',
                          'e_number', 'e_lat', 'e_lng', 'e_name', 'e_name_old']

    # Limiting dataset
    RentalData = RentalData[["BikeNumber", "StartDate", "EndDate",
                             "StartStation", 's_number', "s_lat", "s_lng",
                             "EndStation", 'e_number', 'e_lat', 'e_lng']]

    # Sorting values by rental id = by date
    RentalData.sort_values(by="StartDate", ascending=True, inplace=True)

    # Limiting dataset to rentals from docking stations and to docking staions
    RentalData = RentalData[RentalData['s_lat'] > 0]
    RentalData = RentalData[RentalData['e_lat'] > 0]

    # Resetong index
    RentalData = RentalData.reset_index(drop=True)

    print("Saving to Excel")
    RentalData.to_csv(dir + r'\data\processed\RentalData{}.csv'.format(dataYear), encoding='utf-8', index=False)

if __name__ == "__main__":
    dataYear = input("Please chose year fo analysis (2015 or 2016) \n")
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir, dataYear)