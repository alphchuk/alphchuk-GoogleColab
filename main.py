# Assignment 12 - ANA1001 Python
# Chukwuka Alphonsus
###############################

'''
Q1. Pick two places and download temperature data from the OpenWeather API and save the timestamp. 

Create a dictionary using the following format temps = {“time”:[],“place1”:[],”place2”:[]} 

and save this data to a json file called temps.json.

In order to match up, you will need to write the time, then the two temps, and repeat. Log enough data that you are able to do an analysis over time (perhaps a few minutes of data should work). 

Read the JSON file and create a graph with labels showing both sets of temperature data (y axis) and time series (x axis), make sure to include labels for the chart, x and y axis. Report all temps in C.
'''

import requests
import json
import matplotlib.pyplot as plt
import time
import pygal
import numpy as np
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline
import geopandas
import folium
import pandas as pd


print("Question 1".center(75, "-"),"\n")
apikey = "32f6fb78102b3ad6f99b555b06f475c2" #api key

temps = {} #dictionary for temperature data
lagos = []
sudbury = []
daily_time = []


url_gs = f'https://api.openweathermap.org/data/2.5/forecast?lat=46.49&lon=-80.99&appid={apikey}&units=metric'

url_lg = f'https://api.openweathermap.org/data/2.5/forecast?lat=6.5833&lon=3.75&appid={apikey}&units=metric'

temp_gs = requests.get(url_gs).json()
temp_lg = requests.get(url_lg).json()

from datetime import datetime
ts = int('1284101485')

# print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d'))

for i in temp_lg['list']: #for loop to extract time and temp data from json
  ts = datetime.utcfromtimestamp(i['dt']).strftime('%Y-%m-%d %H:%M:%S')
  daily_time.append(ts)
  lagos.append(i['main']['temp'])
  
for j in temp_gs['list']:  
  sudbury.append(j['main']['temp'])


#print(time)
                                                                    
temps['time'] = daily_time
temps['lagos'] = lagos
temps['sudbury'] = sudbury


with open("temps.json", "w") as fobj: #open json file in write mode
    json.dump(temps, fobj)

readFile = open("temps.json", "r") #read json file
dataJSON = json.load(readFile)
readFile.close

#print(dataJSON)
# plt graph using pyplot
plt.style.use("seaborn")
fig, graphing = plt.subplots()
plt.plot(dataJSON["time"],dataJSON["lagos"], c='red') 
plt.plot(dataJSON["time"],dataJSON["sudbury"], c='blue') 
plt.xlabel("Time") 
plt.ylabel("Temperature (Centigrade)") 
plt.title("Temperature of Lagos and Greater Sudbury") 
plt.savefig('temp.jpg') 
#plt.show()


"""
Q2.     Generate a visualization using JSON data from an API of your choice (not weather related)

"""
print("Question 2".center(75, "-"),"\n")
#import requests
#import json
#import matplotlib.pyplot as plt
#tslaapi = 'q3KiIaVOWOnC0klzXFsuLpSQ36bt8Ss9'
tsla_data = {}
daily_price = []
time = []

#api from poltgon.io
url_tsla = f'https://api.polygon.io/v2/aggs/ticker/TSLA/range/1/day/2021-07-22/2022-05-22?adjusted=true&sort=asc&limit=120&apiKey=q3KiIaVOWOnC0klzXFsuLpSQ36bt8Ss9'

data_json = requests.get(url_tsla).json()

from datetime import datetime

for i in data_json['results'][0:]: #extract daily price using for loop
  daily_price.append(i['c'])


tsla_data['dailyprice'] = daily_price

with open("tesla_trend.json", "w") as fobj: #open json file
    json.dump(tsla_data, fobj)

readFile = open("tesla_trend.json", "r") #read json file
teslaJSON = json.load(readFile)
readFile.close

#print(teslaJSON)
#plot graph
plt.style.use("seaborn")
fig, graphing = plt.subplots()
#plt.plot(teslaJSON["time"],teslaJSON["dailyprice"], c='red') 
plt.plot(teslaJSON["dailyprice"], c='red') 
#plt.xlabel("Time") 
plt.ylabel("Tesla share price (USD)") 
plt.title("One Year Trend of Tesla Share Price") 
plt.savefig('tesla.jpg') 
#plt.show()

'''
Q3 Create a map chart using https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php showing earthquakes in the past seven days for the magnitude level of your choice. See https://python-graph-gallery.com/bubble-map/ and https://python-graph-gallery.com/choropleth-map/ for ideas on how to visualize this type of data.
'''                                                                                                                               
print("Question 3".center(75, "-"),"\n")
#creating empty dictionaries and lists
usgs_7daysdata = {}
lon = []
lat = []
place_name = []
mag = []
id = []

url_usgs = f'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson' #

quakedata_usgs = requests.get(url_usgs).json() 
#Extracting data from json file using for loop, appending to empty lists
for val in quakedata_usgs['features']:
  lon.append(val['geometry']['coordinates'][0])
  lat.append(val['geometry']['coordinates'][1])
  place_name.append(val['properties']['place'])
  mag.append(val['properties']['mag'])
  id.append(val['id'])

#print(lon)
#print(lat)
#print(place_name)
#print(mag)
#print(id)
#creating dictionary form lists
usgs_7daysdata['lon'] = lon
usgs_7daysdata['lat'] = lat
usgs_7daysdata['place name'] = place_name
usgs_7daysdata['magnitude'] = mag
usgs_7daysdata['eq id'] = id
#print(usgs_7daysdata)
#create empty map
m = folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2) #reference below
# Make a data frame with dots to show on the map
eqdata = pd.DataFrame(usgs_7daysdata)

#print(eqdata)
# add marker one by one on the map
for geovalues in range(0,len(eqdata)):
   folium.Circle(
      location=[eqdata.iloc[geovalues]['lat'], eqdata.iloc[geovalues]['lon']],
      popup=eqdata.iloc[geovalues]['place name'],
      radius=float(eqdata.iloc[geovalues]['magnitude'])*20000,
      color='crimson',
      fill=True,
      fill_color='crimson'
   ).add_to(m)

# Show the map again
m
m.save('earthquakedata.html')

'''
 Q4 Using TXT file data from https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms/active-fire-data create a map of global fires within the last seven days. See https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-txt and choose (and note in your file) which dataset you will be using. You can choose from various satellites (MODIS 1km	VIIRS 375m / S-NPP	VIIRS 375m / NOAA-205) See https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-txt and look for World - 24hrs for the data set of your choice. If you have too much data to graph, graph a selection of the data over 1000 rows. Make sure your visualization is on a map.
'''
print("Question 4".center(75, "-"),"\n")
#world VIIRS 375m/NOAA-20
urlviirs = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/csv/J1_VIIRS_C2_Global_24h.csv'
firedata = pd.read_csv(urlviirs)
print(firedata.head())
#ploting map
f = folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2) #reference
#print(eqdata)
# add marker one by one on the map
for geovalues in range(0,len(firedata)):
   folium.Circle(
      location=[firedata.iloc[geovalues]['latitude'], firedata.iloc[geovalues]['longitude']],
      popup=firedata.iloc[geovalues]['version'][0],
      radius=float(firedata.frp.values[0])*1200,
      color='crimson',
      fill=True,
      fill_color='crimson'
   ).add_to(f)

# Show the map again
print(f)
f.save('wildfiredata2.html') #save map

'''
 # The airplane finder program https://repl.it/@SidneyShapiro/AcidicBuzzingMultiprocessing locates flights above a given airport using  the OpenSky API. Edit the program to save data of your choice. Using this data and program, create a chart, build an interactive program, and perform an analysis of the data of your choice. Carefully label and document your code and results so it is understandable..
'''









#References:
#1. https://www.python-graph-gallery.com/313-bubble-map-with-folium