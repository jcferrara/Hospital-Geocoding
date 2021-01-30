#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 13:30:46 2021

@author: JustinFerrara
"""

import requests
import pandas as pd

# Raw data downloaded from https://healthdata.gov/dataset/covid-19-reported-patient-impact-and-hospital-capacity-facility
# Address and zip code data was cleaned in Excel
hhs_facility_data = pd.read_excel('reported_hospital_capacity_admissions_facility_level_weekly_average_timeseries_20210124.xlsx')

# Raw data downloaded from https://public.opendatasoft.com/explore/dataset/us-zip-code-latitude-and-longitude/table/
zipcode_coordinates = pd.read_csv('us-zip-code-latitude-and-longitude.csv', delimiter = ";")


# Census geocoding function: street address to coordinates
def get_census_coordinates(address):
    
    address = [x.replace(" ", "+") for x in address.split(",")]
    url = f'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address={address[0]}%2C{address[1]}%2C{address[2]}&benchmark=9&format=json'
    
    response = requests.get(url)
    response = response.json()
    
    output = (response['result']['addressMatches'][0]['coordinates']['x'], response['result']['addressMatches'][0]['coordinates']['y'])
    
    return(output)
    
# Zip code geocoding: zip code to city centroid
def geocode_zipcode(zip_code):
    
    data = zipcode_coordinates[zipcode_coordinates['Zip'] == zip_code]
    lat = data['Latitude'][0]
    lng =  data['Longitude'][0]
    
    output = (lat, lng)
    
    return(output)
    
# Container for generated coordinates to live before being appended to data frame
coordinates = []
counter = 0

# Loop through each address, generating coordinates for each and holding them in our container
for address in hhs_facility_data['address_cleaned']:
    
    try:
        coordinates.append(get_census_coordinates(address))
    except:
        coordinates.append((0,0))
        
    counter += 1
    print(counter)

# Append coordinates to our data set, separate latitude/longitude into their own columns
hhs_facility_data['Coordinates'] = coordinates
hhs_facility_data['Longitude'] = hhs_facility_data['Coordinates'].apply(lambda x: x[0])
hhs_facility_data['Latitude'] = hhs_facility_data['Coordinates'].apply(lambda x: x[1])

# Export data as CSV to working directory
hhs_facility_data.to_csv('hhs_hospitals.csv', index=False)





