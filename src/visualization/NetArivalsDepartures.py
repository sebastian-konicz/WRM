import folium
from folium.plugins import MarkerCluster
import pandas as pd
from pathlib import Path

pd.options.display.max_columns = 50

def main(dir):
    # Loading Data Set
    print("Loading dataset")
    RentalData = pd.read_csv(dir + r'\data\processed\RentalData.csv',
                        delimiter=",", encoding="utf-8", engine='python', error_bad_lines=False)

    # Changind the StartDate and EndDate to datetime format
    RentalData["StartDate"] = pd.to_datetime(RentalData["StartDate"])
    RentalData["EndDate"] = pd.to_datetime(RentalData["EndDate"])
    RentalData['hour_start'] = RentalData["StartDate"].map(lambda x: x.hour)
    RentalData['hour_end'] = RentalData["StartDate"].map(lambda x: x.hour)

    def get_trip_counts_by_hour(hour):
        # Locations of datastations
        locations = RentalData.groupby("s_number").first()
        locations = locations[["StartStation", "s_lat", "s_lng"]]
        print(locations)

        # Time of day
        subset_start = RentalData[RentalData['hour_start'] == hour]
        subset_end = RentalData[RentalData['hour_end'] == hour]

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

        print(trip_counts)
        # trip_counts.to_csv(dir + r'\data\processed\TripCounts.csv', encoding='utf-8', index=False)
        return trip_counts

    def plot_station_counts(trip_counts):
        # generate a new map
        folium_map = folium.Map(location=[51.110158, 17.031927], zoom_start=13, tiles="CartoDB dark_matter")

        # For each row in the data, add a cicle marker
        for index, row in trip_counts.iterrows():
            # Calculate net departures
            net_departures = (row["DepartureCount"] - row["ArrivalCount"])

            # Popup message that is shown on click.
            popup_text = "{}<br> total departures: {}<br> total arrivals: {}<br> net departures: {}"
            popup_text = popup_text.format(row["StartStation"], row["DepartureCount"], row["ArrivalCount"], net_departures)

            # Radius of circles
            radius = abs(net_departures / 10)

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
                                popup=popup_text,
                                fill=True).add_to(folium_map)
        # Saving map to folder
        folium_map.save(dir + r"\images\NetArivalDepartures.html")
        folium_map.save(dir + r'\Images')
        return folium_map

    trip_counts = get_trip_counts_by_hour(17)
    folium_map = plot_station_counts(trip_counts)

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir)