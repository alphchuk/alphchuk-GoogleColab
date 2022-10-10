import urllib.request
import json
import random
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline
import webbrowser


url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_day.geojson'
response = urllib.request.urlopen(url)
result = json.loads(response.read())

#print(json.dumps(result, indent=4, sort_keys=True)) #prettify json

eq_dict = result['features']
mags, lons, lats, hover = [], [], [], []
for eq in eq_dict:
    mag = eq['properties']['mag']
    lon = eq['geometry']['coordinates'][0]
    lat = eq['geometry']['coordinates'][1]
    title = eq['properties']['title']
    hover.append(title)
    mags.append(mag)
    lons.append(lon)
    lats.append(lat)

print(mags[:5])
print(lons[:5])
print(lats[:5])  

#map the data
data = [{
    'type':'scattergeo',
    'lon': lons,
    'lat': lats,
    'text':hover,
    'marker': {
        'size': [5*mag for mag in mags],
        'color': mags,
        'colorscale': 'Viridis',
        'reversescale': True,
        'colorbar': {'title':'Magnitude'}
    },
}]

my_layout = Layout(title="Global Earthquakes 24hr")

fig = {'data': data, 'layout':my_layout}
offline.plot(fig, filename='eq.html')
webbrowser.open('eq.html')