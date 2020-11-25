import csv
import collections


zip_codes = []

with open('CartoPNPC21_out.csv', newline='\n') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        if row[3] != '':
            zip_codes.append(row[3])


ctr = collections.Counter(zip_codes)


with open('cleaned_out.csv','w',newline='') as writef:
    w = csv.writer(writef, delimiter=';')
    for key,value in ctr.items():
        w.writerow([key,value])