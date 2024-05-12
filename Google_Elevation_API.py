import requests, json
import mysql.connector
import pandas as pd

db = mysql.connector.connect(user = 'root', password = '09122003', host = 'localhost', port = '3306', database = 'test 1')

try:
  file=open("T:\Python\AYD\output.csv","r")
  coordinate=file.readlines() 

except FileNotFoundError:
  print("File coordinate.txt not found!")

apikey= "AIzaSyDoTfYByHuGDc6y6j6-fwyafbOLEx4EGXM"
value = []    

for latlng in coordinate:
  serviceURL = "https://maps.googleapis.com/maps/api/elevation/json?locations="+latlng+"&key="+apikey
  
  r = requests.get(serviceURL)
  print(r.text)
  y = json.loads(r.text)
  for result in y["results"]:
    if result["elevation"] >= 0:
          value.append((result["location"]["lat"], result["location"]["lng"],(result["elevation"])))
    

query = "insert into `coordinate` (`lat`, `lon`, `elevation`) values (%s, %s, %s);"

cursor = db.cursor()
create = "CREATE TABLE IF NOT EXISTS coordinate (lat DECIMAL(9,6),lon DECIMAL(9,6), elevation DECIMAL(9,6));"   
cursor.execute(create)
cursor.executemany(query, value)
db.commit()
  
