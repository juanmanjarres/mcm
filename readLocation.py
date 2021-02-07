import csv
import geopy.distance as di
import location
import sighting_radius as sr
import matplotlib.pyplot as plt
import copy

import libpysal
from libpysal.cg.kdtree import KDTree

import cartopy as cpy
import cartopy.crs as ccrs


data = []
positive_data = []
unverified_data = []
sightings = []


def plot_map():
    # bounds for Washington and South BC
    BOUNDS = [-127.063, -114.034, 45.556, 50.760]
    fig = plt.figure(figsize=(8, 8))
    ax = plt.axes(projection=ccrs.Mercator())
    ax.set_extent(BOUNDS)

    #ax.stock_img()

    ax.add_feature(cpy.feature.LAND)
    ax.add_feature(cpy.feature.COASTLINE)
    ax.add_feature(cpy.feature.OCEAN)

    ax.set_title("Washington/South BC")
    ax.add_feature(cpy.feature.STATES)
    gl = ax.gridlines(linestyle=":", draw_labels=True)
    plt.show()


def check_coord(given_pos_data, given_data_check):
    """

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


def check_near_sightings(loc_x, loc_y):
    # The radius of each sighting.
    # Because the workers often travel at most 8km, we estimate the max distance here
    radius = 8
    loc = loc_x, loc_y
    close = False
    for datapt in positive_data:
        dist = di.distance(datapt.get_loc(), loc).km
        if(dist < radius) and (dist > (-radius)):
            close = True

    if close:
        print("The sighting is nearby a confirmed case")
    else:
        print("The sighting is not near a confirmed case")


with open('/home/juan/Documents/MCM/Locationdata.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count >= 1:
            data.append(location.Location(row[0], row[1], row[2], row[3], row[4]))
        line_count += 1

for point in data:
    if point.get_status() == "Positive ID":
        positive_data.append(point)

for point in data:
    if point.get_status() == "Unverified":
        unverified_data.append(point)

priority_coord = check_coord(positive_data, positive_data)

for i in priority_coord:
    print(i, priority_coord[i])

priority_coord_unver = check_coord(positive_data, unverified_data)

for i in priority_coord_unver:
    print(i, priority_coord_unver[i])

plot_map()

for point in positive_data:
    print(point.to_string())

# Variables for the user location given
location_x = input("Enter the latitude of the location: ")
location_y = input("Enter the longitude of the location: ")

check_near_sightings(location_x, location_y)




