import urlparse # for python 3+ use: from urllib.parse import urlparse
import os
import psycopg2
import sys
import datetime
import re

file_name = sys.argv[1]
db = os.environ.get('DATABASE_URL')


match = re.search(r'.*?\-(.*)_2.*' , file_name)
device_id = match.group(1)
def validate(line):
    try:
        row = line.split('	')
        datetime.datetime.strptime(row[0], '%Y-%m-%d')
        datetime.datetime.strptime(row[1], "%H:%M:%S")
        float(row[2])
        float(row[3])
        float(row[4])
        float(row[5])
        float(row[7])
        float(row[8])
        float(row[9])
        float(row[10])
        return 1
    except ValueError as e:
        print (e)
        return 0

result = urlparse.urlparse(db)
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
connection = psycopg2.connect(
    database = database,
    user = username,
    password = password,
    host = hostname
)
cur = connection.cursor()
with open(file_name, "r+") as script:
    i=0;
    for line in script.readlines():
        if(validate(line)==1):
            try:
                row = line.split('	')
                row = [x.strip(' ') for x in row]
                del row[1]#time
                del row[5]#2D/3D
                del row[6]
                print(row)
                row.insert(0, device_id)
                cur.execute(
                    "INSERT INTO followdem.analyses(device_id, gps_date,ttf,latitude, longitude, sat_number,altitude,hadop,temperature, x, y) "
                    "VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    row
                )
            except ValueError:
                print('error in line :'+ line)
        connection.commit()