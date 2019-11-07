import folium
import selenium.webdriver
import pandas as pd
import time
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
    folium_map = folium.Map(location=[51.110158, 17.031927], zoom_start=12, tiles="CartoDB dark_matter")

    # Plot Markers
    for lat, lng, name, capacity in zip(lat, lng, name, capacity):
        popuptext = str(name) + "<br>" + "Capacity: " + str(capacity)
        popup = folium.Popup(html=popuptext, max_width=250, min_width=150)
        folium.CircleMarker(location=[lat, lng],
                            popup=popup,
                            radius=6,
                            color="#ff3300").add_to(folium_map)

    # Saving the map as html
    path = dir + r"\images\DockingStationsMapBlack.html"
    folium_map.save(path)

    # # # Saving the mas as png
    # driver = selenium.webdriver.PhantomJS(executable_path='C:\\Program Files\\Phantomjs-2.1.1-windows\\bin\\phantomjs')
    # driver.set_window_size(4000, 3000)
    # driver.get(path)
    # time.sleep(100)
    # driver.save_screenshot(dir + r"\images\DockingStationsMapBlack.png")

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir)