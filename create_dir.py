import csv
import os
import shutil

data = []

with open('/home/juan/Documents/MCM/Data_merged.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    line_count = 1
    for row in csv_reader:
        data.append({
            row[1]: row[2]
        })

srcpath = "/home/juan/Downloads/resized/"


