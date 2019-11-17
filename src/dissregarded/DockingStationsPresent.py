import folium
import pandas as pd
from pathlib import Path

def main(dir):
    # Loading Data Set
    DockingStations = pd.read_csv(dir + r'\data\raw\DockingStations.csv',
                                  delimiter=",", encoding="utf-8", engine='python', error_bad_lines=False)
    lat = DockingStations['lat']
    lng = DockingStations['lng']
    name = DockingStations['name']
    capacity = DockingStations['bikes']

    # Create base map
    folium_map = folium.Map(location=[51.099783, 17.03082], zoom_start=12, tiles="CartoDB dark_matter")

    # Plot Markers
    for lat, lng, name, capacity in zip(lat, lng, name, capacity):
        popuptext = str(name) + "<br>" + "Capacity: " + str(capacity)
        popup = folium.Popup(html=popuptext, max_width=250, min_width=150)
        folium.CircleMarker(location=[lat, lng],
                            popup=popup,
                            radius=6,
                            color="#ff3300").add_to(folium_map)

    # Saving the map as html
    pathHTML = dir + r"\images\DockingStationsMapBlack.html"
    folium_map.save(pathHTML)

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir)