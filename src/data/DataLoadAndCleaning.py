import requests
import os
import glob
import pandas as pd
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from pathlib import Path

pd.options.display.max_columns = 50

def main(dir):
    # LOADING DATA FROM DIRECTORY
    # Rental dataset
    dataPath = dir + r'\data\raw'
    datafiles = [file for file in glob.glob(dataPath + r"\Historia*.csv", recursive=True)]

    list_data = []
    for file in datafiles:
        print('Wczytywanie ' + file)
        data = pd.read_csv(file, delimiter=",", encoding="utf-8", engine='python', error_bad_lines=False)
        list_data.append(data)

    # Docking station dataset
    DockingStations = pd.read_csv(dataPath + r'\DockingStations.csv', delimiter=",", encoding="utf-8", engine='python', error_bad_lines=False)
    print(DockingStations)

    # Concatenating rental data
    RentalDataset = pd.concat(list_data, axis=0, ignore_index=True)

    # Dropping duplicate values
    RentalDataset.drop_duplicates(subset="UID wynajmu", inplace=True, keep="first")

    # Merging Rental dataset with Dockin Stations dataset to get geocoordinates of stations
    # Adding geolocation to start station
    RentalDataset = pd.merge(left=RentalDataset, right=DockingStations[['number', 'lat', 'lng', 'name']],
                             left_on="Stacja wynajmu", right_on="name", how='left')
    # Adding geolocation to endstation station
    RentalDataset = pd.merge(left=RentalDataset, right=DockingStations[['number', 'lat', 'lng', 'name']], suffixes=("", "_e"),
                             left_on="Stacja zwrotu", right_on="name", how='left')

    # Renaming columns
    RentalDataset.columns = ["ID", "BikeNumber", "StartDate", "EndDate", "StartStation", "EndStation", "Duration",
                             's_number', "s_lat", "s_lng", 's_name', 'e_number', 'e_lat', 'e_lng', 'e_name']

    # Limiting dataset
    RentalDataset = RentalDataset[["ID", "BikeNumber", "StartDate", "EndDate", "Duration",
                                   "StartStation", 's_number', "s_lat", "s_lng",
                                   "EndStation", 'e_number', 'e_lat', 'e_lng']]

    # Sorting values by rental id = by date
    RentalDataset.sort_values(by="ID", ascending=True, inplace=True)

    # Limiting dataset to rentals from docking stations and to docking staions
    RentalDataset = RentalDataset[RentalDataset['s_lat'] > 0]
    RentalDataset = RentalDataset[RentalDataset['e_lat'] > 0]


    RentalDataset = RentalDataset.reset_index(drop=True)

    print(RentalDataset.tail())
    print("Saving to Excel")
    RentalDataset.to_csv(dir + r'\data\processed\RentalData.csv', encoding='utf-8', index=False)

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir)