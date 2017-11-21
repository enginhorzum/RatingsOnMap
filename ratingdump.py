import sqlite3
import json
import codecs

conn = sqlite3.connect('ratings_db.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM tblRatings')
fhand = codecs.open('ratings.js', 'w', "utf-8")
fhand.write("myData = [\n")
count = 0
for row in cur :
    lat = row[4]
    lng = row[5]
    rating = str(row[3])[:1]
    if lat == 0 or lng == 0 : continue
    if lat is None or lng is None : continue
    where = row[1]
    where = where.replace("'", "")
    try :
        #print(where, rating, lat, lng)

        count = count + 1
        if count > 1 : fhand.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+where+"', " + rating + "]"
        fhand.write(output)
    except:
        continue

fhand.write("\n];\n")
cur.close()
fhand.close()