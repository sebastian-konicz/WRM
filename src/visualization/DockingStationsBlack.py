import folium
from folium.plugins import MarkerCluster
import pandas as pd
from pathlib import Path

def main(dir):
    # Loading Data Set
    DockingStations = pd.read_csv(dir + r'\data\raw\DockingStations.csv',
                                  delimiter=",", encoding="utf-8", engine='python', error_bad_lines=False)
    lat = DockingStations['lat']
    lng = DockingStations['lng']
    name = DockingStations['name']

    # Create base map
    map = folium.Map(location=[51.110158, 17.031927], zoom_start = 14)

    # Plot Marker
    for lat, lng, name in zip(lat, lng, name):
        folium.Marker(location=[lat, lng], popup=str(name),
                  icon=folium.Icon(color='blue', icon='bicycle', prefix='fa')).add_to(map)

    # Save the map
    map.save(dir + r"\images\DockingStationsMap.html")

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir)