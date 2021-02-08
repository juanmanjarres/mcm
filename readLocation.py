import csv
import geopy.distance as di
import location
import sighting_radius as sr
import matplotlib.pyplot as plt
import numpy as np
import datetime

import libpysal
from libpysal.cg.kdtree import KDTree

import cartopy as cpy
import cartopy.crs as ccrs


data = []
positive_data = []
unverified_data = []
sightings = []

def dummy():
    lon = np.linspace(-80, 80, 25)
    lat = np.linspace(30, 70, 25)
    lon2d, lat2d = np.meshgrid(lon, lat)

    data = np.cos(np.deg2rad(lat2d) * 4) + np.sin(np.deg2rad(lon2d) * 4)
    plt.figure(figsize=(6, 3))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    ax.coastlines()
    ax.contourf(lon, lat, data)  # didn't use transform, but looks ok...
    plt.show()



def plot_map(priority):
    # bounds for Washington and South BC
    BOUNDS = [-127.063, -114.034, 45.556, 50.760]
    fig = plt.figure(figsize=(8, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.set_extent(BOUNDS, crs=ccrs.PlateCarree())

    ax.add_feature(cpy.feature.LAND)
    ax.add_feature(cpy.feature.COASTLINE)
    ax.add_feature(cpy.feature.OCEAN)

    ax.set_title("Washington/South BC")
    ax.add_feature(cpy.feature.STATES)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), linestyle=":", draw_labels=True)

    lon = np.linspace(-127.063, -114.034, 50)
    lat = np.linspace(45.556, 50.760, 50)

    lon2d, lat2d = np.meshgrid(lon, lat)

    x = [key[0] for key in priority.keys()]
    y = [key[1] for key in priority.keys()]
    values = [priority[key] for key in priority]

    array = np.zeros(shape=(len(lon)+1, len(lat)+1))

    counter_lon = 0
    counter_lat = 0
    for i in lon:
        for j in lat:
            try:
                array[counter_lon, counter_lat] = priority[(i, j)]
            except KeyError:
                # TODO if it's on an 8km radius, copy the highest value
    #            array[counter_lon, counter_lat] = return_highest_sighting(j, i, priority)
                pass
            counter_lat += 1
        counter_lon += 1

    ax.contourf(lon, lat, array)
    plt.scatter(y, x, values, c='blue', transform=ccrs.PlateCarree())
    plt.show()

    """
    array = np.zeros(shape=(len(x), len(y)))
    for i in range(0, len(x)):
        for j in range(0, len(y)):
            try:
                array[i, j] = priority[(x[i], y[j])]
            except KeyError:
                # TODO if it's on an 8km radius, copy the highest value
                pass
                
    for pt in priority:
        print(pt)
        ax.add_patch(plt.Circle(xy=pt, radius=1000, color='red', alpha=0.3, transform=ccrs.Mercator(), zorder=30))
        # plt.plot(pt[0], pt[1], 'bo', transform=ccrs.Mercator())
    """



def create_priority_dict(given_pos_data, given_data_check):
    """
    Creates a dictionary with the priority for each location in the dictionary based on the given data
    :param given_pos_data: An array containing Location objects with the positive confirmed cases
    :param given_data_check: An array containing Location objects to be checked against positive data
    :return:a dictionary with the keys being a tuple with the location, and the values being the priority value for
            the location
    """
    radius = 8   # radius from the hornets' max range
    priority = {}
    locations = []
    for datapt in given_pos_data:
        locations.append(datapt.get_loc())
        priority[datapt.get_loc()] = 1

    tree = KDTree(locations, distance_metric='Arc', radius=libpysal.cg.RADIUS_EARTH_KM)

    # TODO change the positive data to its own method?
    for datapt in given_pos_data:
        current_point = (datapt.get_loc())

        # get all points within 8km radius
        indices = tree.query_ball_point(current_point, radius)
        for i in indices:
            loc = locations[i]
            if loc in priority:
                priority[loc] += 1

    for datapt in given_data_check:
        current_point = (datapt.get_loc())
        indices = tree.query_ball_point(current_point, radius)
        if len(indices) == 0:
            priority[current_point] = 0

        for i in indices:
            loc = locations[i]
            # Assuming the locations are not repeated
            priority[current_point] = priority[loc]

    return priority


def return_highest_sighting(loc_x, loc_y, dict):
    # The radius of each sighting.
    # Because the workers often travel at most 8km, we estimate the max distance here
    radius = 8
    loc = loc_x, loc_y
    priority = 0
    for key in dict:
        print(key)
        print(loc)
        dist = di.distance(key, loc).km
        if(dist < radius) and (dist > (-radius)):
            if priority < dict[key]:
                priority = dict[key]

    return priority


with open('/home/juan/Documents/MCM/Locationdata.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count >= 1:
            data.append(location.Location(row[0], row[1], row[2], row[3], row[4]))
        line_count += 1

desired_date = input("Input a year for the model: ")


for point in data:
    if point.get_status() == "Positive ID":
        positive_data.append(point)

for point in data:
    if point.get_status() == "Unverified":
        unverified_data.append(point)

dict_positive = create_priority_dict(positive_data, positive_data)

dict_unver = create_priority_dict(positive_data, unverified_data)


plot_map(dict_positive)

#dummy()
# Variables for the user location given
# location_x = input("Enter the latitude of the location: ")
# location_y = input("Enter the longitude of the location: ")

# check_near_sightings(location_x, location_y)




