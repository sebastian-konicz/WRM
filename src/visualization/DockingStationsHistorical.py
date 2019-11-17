import folium
import pandas as pd
from pathlib import Path

def main(dir):
    # Loading dataset
    DockingStations = pd.read_csv(dir + r'\data\processed\RentalData2015.csv')

    # Limiting dataset to unique stations
    DockingStations = DockingStations.groupby('s_number').first()
    DockingStations = DockingStations.reset_index(drop=True)
    print(DockingStations.columns)


    lat = DockingStations['s_lat']
    lng = DockingStations['s_lng']
    name = DockingStations['StartStation']
    # capacity = DockingStations['bikes']

    # Create base map
    folium_map = folium.Map(location=[51.110158, 17.031927], zoom_start=13, tiles="CartoDB dark_matter")

    # Plot Markers
    for lat, lng, name in zip(lat, lng, name):
        popuptext = str(name)
        popup = folium.Popup(html=popuptext, max_width=250, min_width=150)
        folium.CircleMarker(location=[lat, lng],
                            popup=popup,
                            radius=6,
                            color="#ff3300").add_to(folium_map)

    # Saving the map as html
    pathHTML = dir + r"\images\DockingStationsMapBlack2015.html"
    folium_map.save(pathHTML)

    return folium_map


if __name__ == "__main__":
    # dataYear = input("Please chose year fo analysis (2015 or 2016) \n")
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir)