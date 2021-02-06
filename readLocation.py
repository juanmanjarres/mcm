import csv
import geopy.distance as di
import location

data = []
positive_data = []


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

for point in positive_data:
    print(point.to_string())

# Variables for the user location given
location_x = input("Enter the latitude of the location: ")
location_y = input("Enter the longitude of the location: ")

check_near_sightings(location_x, location_y)




