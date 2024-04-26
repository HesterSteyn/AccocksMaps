import csv
import folium
import webbrowser

filename = 'AcocksExport20240405_090419.csv' 
keys = ('Barcode', 'Latitude', 'Longitude', 'Date')
records = []


#read the data from csv file into dictionary
with open (filename, 'r') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    records.append({key: row[key] for key in keys})

# for record in records:
#   x = float(record['Latitude'])
#   print(type(x))
#   y = float(record['Longitude'])
#   coords = (x, y)

map = folium.Map(location=[-29.265047, 24.959101], zoom_start=6)

for record in records:
    latitude_str = record['Latitude']
    longitude_str = record['Longitude']
    
    # print(f"Latitude: {latitude_str}, Longitude: {longitude_str}")

    try:
        x = float(latitude_str)
        y = float(longitude_str)
        coords = (x, y)
        
        #create markers
        folium.Marker(coords, 
                      popup = record['Barcode']).add_to(map)

    except ValueError as e:
        print(f"Error converting to float: {e}")

#generate and display map
map.save('acocks.html')
webbrowser.open("acocks.html")
        


# print(records[0])


