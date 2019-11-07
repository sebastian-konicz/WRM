from PIL import Image, ImageDraw
import numpy as np
import pandas as pd
import folium
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.colors import LinearSegmentedColormap, rgb_to_hsv, hsv_to_rgb
import scipy.ndimage.filters
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

    # Getting geolocation data
    min_lat = RentalData["s_lat"].min()
    max_lat = RentalData["s_lat"].max()
    max_lon = RentalData["s_lng"].max()
    min_lon = RentalData["s_lng"].min()

    # Kerner for convolution
    def get_kernel(kernel_size, blur=1 / 20, halo=.001):
        """
        Create an (n*2+1)x(n*2+1) numpy array. Output can be used as the kernel for convolution.
        """
        # generate x and y grids
        x, y = np.mgrid[0:kernel_size * 2 + 1, 0:kernel_size * 2 + 1]

        center = kernel_size + 1  # center pixel
        r = np.sqrt((x - center) ** 2 + (y - center) ** 2)  # distance from center

        # now compute the kernel. This function is a bit arbitrary.
        # adjust this to get the effect you want.
        kernel = np.exp(-r / kernel_size / blur) + (1 - r / r[center, 0]).clip(0) * halo
        return kernel

    # Adding lines
    def add_lines(image_array, xys, width=1, weights=None):
        """
        Add a set of lines (xys) to an existing image_array width: width of lines
        weights: [], optional list of multipliers for lines.
        """
        for i, xy in enumerate(xys):  # loop over lines
            # create a new gray scale image
            image = Image.new("L", (image_array.shape[1], image_array.shape[0]))

            # draw the line
            ImageDraw.Draw(image).line(xy, 200, width=width)

            # convert to array
            new_image_array = np.asarray(image, dtype=np.uint8).astype(float)

            # apply weights if provided
            if weights is not None:
                new_image_array *= weights[i]

            # add to existing array
            image_array += new_image_array

        # convolve image
        new_image_array = scipy.ndimage.filters.convolve(image_array, get_kernel(width * 4))
        return new_image_array

    #  Converting array of floats to array of RGB values
    def to_image(array, hue=.62):
        """converts an array of floats to an array of RGB values using a colormap"""

        # apply saturation function
        image_data = np.log(array + 1)

        # create colormap, change these values to adjust to look of your plot
        saturation_values = [[0, 0], [1, .68], [.78, .87], [0, 1]]
        colors = [hsv_to_rgb([hue, x, y]) for x, y in saturation_values]
        cmap = LinearSegmentedColormap.from_list("my_colormap", colors)

        # apply colormap
        out = cmap(image_data / image_data.max())

        # convert to 8-bit unsigned integer
        out = (out * 255).astype(np.uint8)
        return out

        # Convert Latitude and Longitude to Pixel Coordinates

    def latlon_to_pixel(lat, lon, image_shape):
        # longitude to pixel conversion (fit data to image)
        delta_x = image_shape[1] / (max_lon - min_lon)

        # latitude to pixel conversion (maintain aspect ratio)
        delta_y = delta_x / np.cos(lat / 360 * np.pi * 2)
        pixel_y = (max_lat - lat) * delta_y
        pixel_x = (lon - min_lon) * delta_x
        return (pixel_y, pixel_x)

    def row_to_pixel(row, image_shape):
        """
        convert a row (1 trip) to pixel coordinates
        of start and end point
        """
        start_y, start_x = latlon_to_pixel(row["s_lat"],
                                           row["s_lng"], image_shape)
        end_y, end_x = latlon_to_pixel(row["e_lat"],
                                       row["e_lng"], image_shape)
        xy = (start_x, start_y, end_x, end_y)
        return xy

    def add_alpha(image_data):
        """
        Uses the Value in HSV as an alpha channel.
        This creates an image that blends nicely with a black background.
        """

        # get hsv image
        hsv = rgb_to_hsv(image_data[:, :, :3].astype(float) / 255)

        # create new image and set alpha channel
        new_image_data = np.zeros(image_data.shape)
        new_image_data[:, :, 3] = hsv[:, :, 2]

        # set value of hsv image to either 0 or 1.
        hsv[:, :, 2] = np.where(hsv[:, :, 2] > 0, 1, 0)

        # combine alpha and new rgb
        new_image_data[:, :, :3] = hsv_to_rgb(hsv)
        return new_image_data

    # Trips for one time of the day
    def get_image_data_trips_day():
        paths = RentalData[RentalData['hour_start'] == 7]
        paths = paths.iloc[:3000, :]
        print(paths.shape)

        # generate empty pixel array, choose your resolution
        image_data = np.zeros((1000, 1000))

        # generate pixel coordinates of starting points and end points
        xys = [row_to_pixel(row, image_data.shape) for i, row in paths.iterrows()]

        # draw the lines
        image_data = add_lines(image_data, xys, weights=None, width=1)
        return image_data

    def unique_paths(time_of_day, trip_count):
        # make a list of locations (latitude longitude) for each station id
        locations = RentalData.groupby("s_number").mean()
        locations = locations.loc[:, ["s_lat", "s_lng"]]

        # group by each unique pair of (start-station, end-station) and count the number of trips
        RentalData["path_id"] = [(id1, id2) for id1, id2 in zip(RentalData["s_number"], RentalData["e_number"])]

        paths = RentalData[RentalData["hour_start"] == time_of_day].groupby("path_id").count().iloc[:, [1]]
        paths.columns = ["Trip Count"]

        # select only paths with more than X trips
        paths = paths[paths["Trip Count"] > trip_count]
        paths["s_number"] = paths.index.map(lambda x: x[0])
        paths["e_number"] = paths.index.map(lambda x: x[1])
        paths = paths[paths["s_number"] != paths["e_number"]]

        # join latitude/longitude into new table
        paths = paths.join(locations, on="s_number")
        locations.columns = ["e_lat", "e_lng"]
        paths = paths.join(locations, on="e_number")
        paths.index = range(len(paths))
        return paths

    def get_image_data(paths, min_count=0, max_count=None):
        # generate empty pixel array
        image_data = np.zeros((1000 * 2, 1000 * 2))

        # generate pixel coordinates of starting points and end points
        if max_count is None:
            max_count = paths["Trip Count"].max() + 1
        selector = (paths["Trip Count"] >= min_count) & (paths["Trip Count"] < max_count)
        xys = [row_to_pixel(row, image_data.shape) for i, row in paths[selector].iterrows()]

        # draw the lines
        image_data = add_lines(image_data, xys, weights=paths["Trip Count"], width=1)
        return image_data

    # create the map
    def folium_map(time_of_day, trip_count):
        folium_map = folium.Map(location=[51.110158, 17.031927],
                                zoom_start=13,
                                tiles="CartoDB dark_matter")

        # create the overlay
        map_overlay = add_alpha(to_image(get_image_data(unique_paths(time_of_day, trip_count)) * 10))
        # map_overlay = add_alpha(to_image(get_image_data_trips_day() * 10))

        # compute extent of image in lat/lon
        aspect_ratio = map_overlay.shape[1] / map_overlay.shape[0]
        delta_lat = (max_lon - min_lon) / aspect_ratio * np.cos(min_lat / 360 * 2 * np.pi)

        # add the image to the map
        img = folium.raster_layers.ImageOverlay(map_overlay,
                                                bounds=[(max_lat - delta_lat, min_lon), (max_lat, max_lon)],
                                                opacity=1,
                                                name="Paths")

        img.add_to(folium_map)
        folium.LayerControl().add_to(folium_map)
        folium_map.save(dir + r"\images\Paths{}.html".format(time_of_day))

    for time in range(25):
        print(time)
        folium_map(time, 1)

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir)