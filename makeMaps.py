from os import path
import time
from datetime import datetime
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import matplotlib.pyplot as plt
from geopandas import GeoDataFrame
from progress.bar import Bar

# Read the CSV file with points
print('reading csv data')
csv_name = 'AcocksExport20240426_OR.csv'
points_df = pd.read_csv(csv_name)
uniquedates = list(set(points_df['Date']))
validuniquedates = list(filter(lambda x: isinstance(x, str) and r'/' in x and len(x.split('/')) == 3, uniquedates))
fixeddates = list(map(lambda x: str(datetime.strptime(x, '%m/%d/%Y')).split(' ')[0], validuniquedates))
fixeddates.sort()
firstdateindex = fixeddates.index(next(x for x in fixeddates if int(x.split('-')[0]) >= 1936)) 
lastdateindex = fixeddates.index(next(x for x in fixeddates if int(x.split('-')[0]) >= 1977))
searchdates = fixeddates[firstdateindex : lastdateindex]

#we need to add the corrected dates in the dataframe so we can filter later
points_df['FormattedDate'] = None
for index, row in points_df.iterrows():
  if isinstance(row['Date'], str) and r'/' in row['Date'] and len(row['Date'].split('/')) == 3:
    points_df.at[index, 'FormattedDate'] = str(datetime.strptime(row['Date'], '%m/%d/%Y')).split(' ')[0]

# Read the shapefile
print('reading country shapefile')
shapefile_path = r'C:\GISData\GISData\admin'
shapefile_name = r'SA_PROV_2016_KZN_clip.shp'
gdf = gpd.read_file(path.join(shapefile_path, shapefile_name))

# Plot the shapefile
print('plotting country shapefile')
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color='white', edgecolor='black')



# Plot the points on the same map
# print('plotting csv data')
geometry = [Point(xy) for xy in zip(points_df['Longitude'], points_df['Latitude'])]
points_gdf = GeoDataFrame(points_df, geometry=geometry)
points_gdf.plot(ax=ax, color='lightgray', marker='o', markersize=5)

# # Customize the map appearance if needed
# ax.set_title('Shapefile with Points Overlay')
# ax.set_xlabel('Longitude')
# ax.set_ylabel('Latitude')
bar = Bar('Mapping', max=len(searchdates))
for date in searchdates:
  daterecords = points_gdf[points_gdf['FormattedDate'] == date]
  daterecords.plot(ax=ax, color='red', marker='o', markersize=8)
  #Save the map as a JPEG
  output_path = date + '.jpg'
  plt.savefig(path.join('maps',output_path), format='jpeg', dpi=300)
  daterecords.plot(ax=ax, color='lightgrey', marker='o', markersize=5)
  bar.next()

bar.finish()
print('all done!')

# Display the map
plt.show()
