import csv
import geopy.distance
import location

data = []

with open('/home/juan/Documents/MCM/Locationdata.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count >= 1:
            data.append(location.Location(row[0], row[1], row[2], row[3], row[4]))
        line_count += 1

    for point in data:
        print(point.to_string())




