import streamlit as st
import pandas as pd
from urllib.parse import quote_plus
import pymongo
from pymongo import MongoClient
import certifi

@st.cache_resource
def init_connection():
    ca_cert_bundle = certifi.where()  
    username = 'bt22cse089'
    password = 'aayush@123'
    encoded_password = quote_plus(password)
    connection_string = f'mongodb+srv://{username}:{encoded_password}@for-testing.ocsya6p.mongodb.net/?retryWrites=true&w=majority&appName=For-testing&tlsCAFile={ca_cert_bundle}'
    return MongoClient(connection_string)

client = init_connection()
db = client["VehicleMaintenance"]
collection = db["VehicleReading"]

logo_path = "/Users/aayushjain/codes/projects/company assignements/Snape/City Heatmap/MLOPS/snape_logo.png"
st.logo(logo_path)  # Change st.logo to st.image
st.title("Weekly Maintenance -SNAPE")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)
    
    for index, row in df.iterrows():
        vehicle_number = row["Vehicle Number"]
        current_reading = row["CurrentReading"]
        
        collection.update_one(
            {"Vehicle Number": vehicle_number},
            {"$set": {"current_reading": current_reading}}
        )
    
    result = []
    for index, row in df.iterrows():
        vehicle_number = row["Vehicle Number"]
        current_reading = row["CurrentReading"]
        
        vehicle = collection.find_one({"Vehicle Number": vehicle_number})
        if vehicle:
            base_reading = vehicle["Closing KM"]
            difference = current_reading - base_reading
            modulo_difference = difference % 12000
            if 0 <= modulo_difference <= 500 or 11500 <= modulo_difference <= 11999:
                result.append(vehicle_number)
    
    st.write("Vehicles due for maintenance:", result)

col1, col2 = st.columns(2)
with col1:
    show_create_form = st.button("Add New Vehicle")
with col2:
    show_delete_form = st.button("Delete Vehicle")

# Create new vehicle record
if show_create_form:
    st.header("Add New Vehicle")
    new_vehicle_number = st.text_input("Vehicle Number")
    new_closing_km = st.number_input("Closing KM", min_value=0)
    create_button = st.button("Create")
    if create_button:
        if new_vehicle_number and new_closing_km >= 0:
            collection.insert_one({
                "Vehicle Number": new_vehicle_number,
                "Closing KM": new_closing_km,
                "current_reading": new_closing_km
            })
            st.success(f"Vehicle {new_vehicle_number} added successfully.")
        else:
            st.error("Please enter valid data.")

# Delete existing vehicle record
if show_delete_form:
    st.header("Delete Vehicle")
    delete_vehicle_number = st.text_input("Vehicle Number to Delete")
    delete_button = st.button("Delete")
    if delete_button:
        if delete_vehicle_number:
            result = collection.delete_one({"Vehicle Number": delete_vehicle_number})
            if result.deleted_count > 0:
                st.success(f"Vehicle {delete_vehicle_number} deleted successfully.")
            else:
                st.error(f"Vehicle {delete_vehicle_number} not found.")
        else:
            st.error("Please enter a valid Vehicle Number.")