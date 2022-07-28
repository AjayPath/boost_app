# Created by Ajay Path
# Date July 2022

# This file is used to create the map used on the HTML site.

import folium
from IPython.display import display

map = folium.Map(
    location = [0, 0],
    zoom_start = 4,
    tiles='Stamen Terrain'
)

fgp = folium.FeatureGroup(name = "site_locations")

fgp.add_child(folium.Marker(location=[7.737800, -2.104910], popup = 'Wenchi', tooltip = 'Wenchi'))
map.add_child(fgp)

fgp.add_child(folium.Marker(location=[11.894070, 105.958660], popup = 'Steung Chrov', tooltip = 'Steung Chrov'))
map.add_child(fgp)

fgp.add_child(folium.Marker(location=[33.90745, 76.82912], popup = 'Lingshed Monastary', tooltip = 'Lingshed Monastary'))
map.add_child(fgp)

map.save("map.html")

print("done")



