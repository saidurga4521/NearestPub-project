# import all required liberaries
import numpy as np
import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from folium import Marker
from streamlit_folium import folium_static

#Load the pub dataset
pub_data=pd.read_csv('open_pubs.csv',header=None)
pub_data.columns = ['fsa_id', 'name', 'address', 'postcode', 'easting', 'northing', 'latitude', 'longitude', 'local_authority']

# handling the null values
pub_data=pub_data.replace('//N',np.nan)
# Drop the rows with null values
pub_data=pub_data.dropna()

pub_data['longitude'] = pd.to_numeric(pub_data['longitude'], errors='coerce')
pub_data['latitude'] = pd.to_numeric(pub_data['latitude'], errors='coerce')

# set the page layout to centred

st.set_page_config('centered')

# Add some styling to the title and subtitle
st.markdown("<h1 style='text-align: center; color: #EB6864; font-weight: bold;'>🍺  Nearest Pubs Application 🍻</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #5243AA;'>Welcome to our pub finder app! 🎉</h2>", unsafe_allow_html=True)

# Allow user to enter the lat and long
# Allow user to enter their latitude and longitude
lat = st.number_input("Enter your latitude:", value=51.73)
lon = st.number_input("Enter your longitude:", value=-4.72)

#Define a function to calculate the euclidian distance

def euclidean(lat1,long1,lat2,long2):
    return np.sqrt((lat1-lat2)**2+(long1-long2)**2)

# Now calculate the distance between the user inputs and each point in the dataset
pub_data['distance']=pub_data.apply(lambda row:euclidean(row['latitude'], row['longitude'], lat, lon), axis=1)

# Sort the dataset by distance and display the nearest 5 pubs
nearest_pubs = pub_data.sort_values(by='distance').head(5)
st.write(f"Displaying the 5 nearest pubs to your location (lat: {lat}, lon: {lon}):")
st.dataframe(nearest_pubs)

# Create a map centered on the user's location
m = folium.Map(location=[lat, lon], zoom_start=13)

# Add a marker for the user's location
folium.Marker(location=[lat, lon], icon=folium.Icon(color='red'), popup='Your Location').add_to(m)

# Add markers for each of the nearest pubs
marker_cluster = MarkerCluster().add_to(m)
for index, row in nearest_pubs.iterrows():
    Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(marker_cluster)

# Display the map
st.write("Map of the nearest pubs:")
folium_static(m)