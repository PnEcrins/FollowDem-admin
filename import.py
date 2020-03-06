from urllib.parse import urlparse
import os
import psycopg2
import sys
import datetime
import re
import csv
from conf import SQLALCHEMY_DATABASE_URI

file_name = sys.argv[1]
db = SQLALCHEMY_DATABASE_URI

# Return device id : fisrt match between  caracters - and _
match = re.search(r'\-(.*?)\_', file_name)
device_id = match.group(1)

def validate(line):
    try:
        datetime.datetime.strptime(line[0], '%Y-%m-%d')
        datetime.datetime.strptime(line[1], "%H:%M:%S")
        float(line[2])
        float(line[3])
        float(line[4])
        float(line[5])
        float(line[7])
        float(line[8])
        float(line[9])
        float(line[10])
        return 1
    except ValueError as e:
        print (e)
        return 0

def format_to_timestamp(str_date, str_time):
    dt = datetime.datetime.strptime(str_date,'%Y-%m-%d')
    tm = datetime.datetime.strptime(str_time, '%H:%M:%S').time()
    return datetime.datetime.combine(dt, tm).strftime('%Y-%m-%d %H:%M:%S')

result = urlparse(db)
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

with open(file_name, "r", encoding="utf8", errors='ignore') as f:
    # delimiter tab
    reader = csv.reader(f, delimiter='\t')
    next(reader)
    for line in reader:
        line = [x.strip(' ') for x in line]
        if(len(line) > 0 and validate(line)==1):
            try:
                line[0] = format_to_timestamp(line[0], line[1])
                del line[1]#time
                del line[5]#2D/3D
                del line[8]#x
                del line[8]#y
                line.insert(0, device_id)
                cur.execute(
                    "INSERT INTO followdem.t_gps_data(id_device, gps_date, ttf, latitude, longitude, sat_number, altitude, hdop, temperature) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    line
                )
            except ValueError:
                print('error in line :'+ line)
        connection.commit()