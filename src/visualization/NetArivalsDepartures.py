import folium
from PIL import Image, ImageDraw, ImageFont
import io
from folium.plugins import MarkerCluster
import pandas as pd
import datetime
from pathlib import Path

# pd.options.display.max_columns = 50

def main(dir):
    # Loading Data Set
    print("Loading dataset")
    RentalData = pd.read_csv(dir + r'\data\processed\RentalData2015.csv')

    # Changind the StartDate and EndDate to datetime format
    RentalData["StartDate"] = pd.to_datetime(RentalData["StartDate"])
    RentalData["EndDate"] = pd.to_datetime(RentalData["EndDate"])
    RentalData['hour_start'] = RentalData["StartDate"].map(lambda x: x.hour)
    RentalData['hour_end'] = RentalData["StartDate"].map(lambda x: x.hour)

    # Excluding form computation trips made between the same station
    RentalData = RentalData[RentalData['StartStation'] != RentalData['EndStation']]
    RentalData = RentalData.reset_index(drop=True)
    print(RentalData.tail())

    def get_trip_counts_by_hour(hour_start, hour_end):
        # Locations of datastations
        locations = RentalData.groupby("s_number").first()
        locations = locations[["StartStation", "s_lat", "s_lng"]]

        # Time of day
        subset_start = RentalData[(RentalData['hour_start'] >= hour_start) & (RentalData['hour_start'] <= hour_end)]
        subset_end = RentalData[(RentalData['hour_start'] >= hour_start) & (RentalData['hour_start'] <= hour_end)]

        # Counting trips FROM docking station (departures)
        departure_counts = subset_start.groupby("StartStation").count().iloc[:, [0]]
        departure_counts.columns = ['DepartureCount']

        # Counting trips TO docking station (arrivals)
        arrival_counts = subset_end.groupby("EndStation").count().iloc[:, [0]]
        arrival_counts.columns = ["ArrivalCount"]

        # Joining departure counts and arrival counts
        trip_counts = departure_counts.join(arrival_counts)

        # Merging with locations to get latitude and longitude of station
        trip_counts = pd.merge(trip_counts, locations, on="StartStation")

        # trip_counts.to_csv(dir + r'\data\processed\TripCounts.csv', encoding='utf-8', index=False)
        return trip_counts

    def plot_station_counts(trip_counts, time_of_day, zoom_start=13):
        # generate a new map
        folium_map = folium.Map(location=[51.099783, 17.03082], zoom_start=zoom_start, tiles="CartoDB dark_matter")

        # For each row in the data, add a cicle marker
        for index, row in trip_counts.iterrows():
            # Calculate net departures
            net_departures = (row["DepartureCount"] - row["ArrivalCount"])

            # Popup message that is shown on click.
            popuptext = "{}<br> total departures: {}<br> total arrivals: {}<br> net departures: {}"
            popuptext = popuptext.format(row["StartStation"], row["DepartureCount"], row["ArrivalCount"], net_departures)
            popup = folium.Popup(html=popuptext, max_width=250, min_width=150)

            # Radius of circles
            radius = 6

            # Color of the marker
            if net_departures > 0:
                # color="#FFCE00" # orange / # color="#007849" # green
                color = "#E37222"  # tangerine
            else:
                # color="#0375B4" # blue / # color="#FFCE00" # yellow
                color = "#0A8A9F"  # teal

            # add marker to the map
            folium.CircleMarker(location=(row["s_lat"], row["s_lng"]),
                                radius=radius,
                                color=color,
                                popup=popup,
                                fill=True).add_to(folium_map)
        # Saving map to folder
        folium_map.save(dir + r"\images\sites\NetArivalDepartures-{}.html".format(time_of_day))
        return folium_map

    def image_save(hour_start, hour_end, save_path, time_of_day):
        # create the map object
        data = get_trip_counts_by_hour(hour_start, hour_end)
        my_frame = plot_station_counts(data, time_of_day, zoom_start=13)

        # generate the png file as a byte array
        png = my_frame._to_png()

        # create a PIL image object
        image = Image.open(io.BytesIO(png))
        draw = ImageDraw.ImageDraw(image)

        # # load a font
        # font = ImageFont.truetype("arial.ttf", 30)

        # text = "Net Arrivals/Departures in the " + time_of_day
        # # draw title
        # draw.text((image.width - 900, 20),
        #           text,
        #           fill=(255, 255, 255),
        #           font=font)

        # write to a png file
        filename = save_path + r"\NetArivalsDepartures-{}.png".format(time_of_day)
        image.save(filename, "PNG")
        return image

    save_path= dir + r'\images\final'
    image_save(5, 9, save_path, "morning")
    image_save(15, 19, save_path, "afternoon")

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir)