import folium
from PIL import Image, ImageDraw, ImageFont
import io
import pandas as pd
from pathlib import Path

def main(dir):
    # Loading dataset
    DockingStations = pd.read_csv(dir + r'\data\processed\RentalData2015.csv')

    # Limiting dataset to unique stations
    DockingStations = DockingStations.groupby('s_number').first()
    DockingStations = DockingStations.reset_index(drop=True)

    def folium_map():
        lat = DockingStations['s_lat']
        lng = DockingStations['s_lng']
        name = DockingStations['StartStation']
        # capacity = DockingStations['bikes']

        # Create base map
        folium_map = folium.Map(location=[51.099783, 17.03082], zoom_start=13, tiles="CartoDB dark_matter")

        # Plot Markers
        for lat, lng, name in zip(lat, lng, name):
            popuptext = str(name)
            popup = folium.Popup(html=popuptext, max_width=250, min_width=150)
            folium.CircleMarker(location=[lat, lng],
                                popup=popup,
                                radius=6,
                                color="#ff3300").add_to(folium_map)

        # Saving the map as html
        pathHTML = dir + r"\images\sites\DockingStationsMap.html"
        folium_map.save(pathHTML)

        return folium_map

    def image_save(map):
        # generate the png file as a byte array
        png = map._to_png()

        # create a PIL image object
        image = Image.open(io.BytesIO(png))

        # write to a png file
        pathImage = dir + r"\images\final\DockingStationsMap.png"
        image.save(pathImage, "PNG")
        return image

    map = folium_map()
    image_save(map)

if __name__ == "__main__":
    # dataYear = input("Please chose year fo analysis (2015 or 2016) \n")
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir)