import csv
import geopy.distance as di
import location
import sighting_radius as sr
import matplotlib.pyplot as plt
import cartopy as cpy
import cartopy.crs as ccrs

data = []
positive_data = []
sightings = []


def plot_map():
    # bounds for the state of washington
    BOUNDS = [-124.849, -116.9156, 45.5435, 49.0024]
    fig = plt.figure(figsize=(8, 8))
    ax = plt.axes(projection=ccrs.Mercator())
    ax.set_extent(BOUNDS)
    ax.set_title("Washington")
    ax.add_feature(cpy.feature.STATES)
    gl = ax.gridlines(linestyle=":", draw_labels=True)
    plt.show()



def locate_nests():
    for datapt in positive_data:
        sightings.append(sr.SightingRadius(datapt.get_loc(), 8, 1))


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

plot_map()

for point in positive_data:
    print(point.to_string())

# Variables for the user location given
location_x = input("Enter the latitude of the location: ")
location_y = input("Enter the longitude of the location: ")

check_near_sightings(location_x, location_y)




