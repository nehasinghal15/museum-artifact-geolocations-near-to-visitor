import os
import pandas as pd
import numpy as np
import sys
from distutils.sysconfig import get_python_lib

print(get_python_lib())
#sys.path.append("/Users/neha/opt/anaconda3/lib/python3.9/site-packages/")#path to my python packages. you can delete this line if it shows an error in your system
sys.path.append(get_python_lib())#path to my python packages. you can delete this line if it shows an error in your system
print(os.getcwd())
#goal_dir = os.path.join(os.getcwd(), "../../Finding nearest cities to user city in DE/GeoNames_DE.xlsx")
base_cities=pd.read_excel(r'./../Finding nearest cities to user city in DE/GeoNames_DE.xlsx')
cities = pd.read_excel(r'./../Finding nearest cities to user city in DE/LMW_Orte_mit_Geokoordinaten.xlsx')
print(cities.dtypes)
flag=0

#latitude and longitudes are in decimal degrees with latitude(-90 to +90) and longitude(-180 to +180) 

#finding distances using Haversine formula
#https://towardsdatascience.com/heres-how-to-calculate-distance-between-2-geolocations-in-python-93ecab5bbba4
def haversine_distance(lat1, lon1, lat2, lon2):
   r = 6371
   phi1 = np.radians(lat1) #convert decimal degrees to radians
   #print(type(lat1))
   phi2 = np.radians(lat2)
   delta_phi = np.radians(lat2-lat1)
   delta_lambda = np.radians(lon2-lon1)
   a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
   res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1-a)))
   return np.round(res, 2)

string='distance from '
city= input('enter the city')
#print(type(city))

#search for the city entered by user, in the excel file GeoNames_DE
for index, row in base_cities.iterrows():
    if (row['name'] == city): #if the city entered by user is found in the in the excel file,'GeoNames_DE'
        print('city is', city)
        start_lat = row['latitude'] #get lat
        start_lon = row['longitude'] #get longitude
        flag=1
        break #this will exit the loop once the city is matched with user's input

if flag==1: #means the user's city is found in the excel file GeoNames_DE
    distances_km = [] #create an empty column that will be later added to the dataframe of excel file, 'LMW_Orte_mit_Geokoordinaten' 
    for row in cities.itertuples(index=False): #iterate through rows of excel file, 'LMW_Orte_mit_Geokoordinaten' for calculating distances with respect to user's entered city
        distances_km.append(
       haversine_distance(start_lat, start_lon, row.LATITUDE, row.LONGITUDE)
       )#append the distances of each city with respect to the user's entered city
    city_dist= string + city #for renaming the distance column, i am appending the user input ciy with a string, 'distance from'. eg. distance from <Zwönitz>.
    cities[city_dist] = distances_km #appending a new column of distance wrt the entered city by user
    cities= cities.sort_values(city_dist)
    cities.to_excel('distances_geolocations_stuttgart.xlsx')
    print('the nearest locations around your entered city', city, 'with latitude', start_lat, 'and as longitude', start_lon, 'are')
    #print the 5 nearest cities around the user's city
    for index,row in cities.iloc[:5].iterrows(): 
        print(row['NAME'])
else:
    print('the city not found. Enter new city')

