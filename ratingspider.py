from urllib.request import urlopen
import urllib.error
import ratingurl
import json
import sqlite3
import ssl
import requests
import time

conn = sqlite3.connect('ratings_db.sqlite')
cur = conn.cursor()

cur.execute('''
            CREATE TABLE IF NOT EXISTS tblRatings
            (Id TEXT PRIMARY KEY, Name TEXT, ReviewCount INTEGER, Rating DOUBLE, Lat TEXT, Lon TEXT)''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

DEFAULT_TERM = 'restaurants'
DEFAULT_LOCATION = 'london'

offset = 1
while True : 
    if ( offset >= 200 ) :
        conn.commit()
        print('Retrieved ' + str(offset) + ' records.')
        break

    data = ratingurl.query_api(DEFAULT_TERM, DEFAULT_LOCATION, offset)

    for u in data['businesses']:
        b_id = u['id']
        b_name = u['name']
        review_count = u['review_count']
        rating = u['rating']
        lat = u['coordinates']['latitude']
        lon = u['coordinates']['longitude']
        
        cur.execute('''INSERT OR IGNORE INTO tblRatings (Id, Name, ReviewCount, Rating, Lat, Lon)
                    VALUES (?, ?, ?, ?, ?, ?)''', (b_id, b_name, review_count, rating, lat, lon))
        conn.commit()
        offset = offset + 1;
        
    
    print('Next query start at',offset)
    print('Pausing for a bit...')
    time.sleep(5)  
             

cur.close()
