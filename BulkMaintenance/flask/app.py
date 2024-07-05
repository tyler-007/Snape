from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from urllib.parse import quote_plus
from pymongo import MongoClient
import certifi

app = Flask(__name__)

# MongoDB connection setup
username = 'bt22cse089'
password = 'aayush@123'
encoded_password = quote_plus(password)
ca_cert_bundle = certifi.where()
connection_string = f'mongodb+srv://{username}:{encoded_password}@for-testing.ocsya6p.mongodb.net/?retryWrites=true&w=majority&appName=For-testing&tlsCAFile={ca_cert_bundle}'
client = MongoClient(connection_string)
db = client["VehicleMaintenance"]
collection = db["VehicleReading"]

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_csv(file)
            vehicles_due_for_maintenance = process_data(df)
            return render_template('upload.html', df=df, vehicles_due=vehicles_due_for_maintenance)
    return render_template('upload.html')

def process_data(df):
    result = []
    for index, row in df.iterrows():
        vehicle_number = row["Vehicle Number"]
        current_reading = row["CurrentReading"]
        
        collection.update_one(
            {"Vehicle Number": vehicle_number},
            {"$set": {"current_reading": current_reading}}
        )
        
        vehicle = collection.find_one({"Vehicle Number": vehicle_number})
        if vehicle:
            base_reading = vehicle["Closing KM"]
            difference = current_reading - base_reading
            modulo_difference = difference % 12000
            if 0 <= modulo_difference <= 500 or 11500 <= modulo_difference <= 11999:
                result.append(vehicle_number)
    
    return result

@app.route('/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        vehicle_number = request.form['vehicle_number']
        closing_km = int(request.form['closing_km'])
        
        collection.insert_one({
            "Vehicle Number": vehicle_number,
            "Closing KM": closing_km,
            "current_reading": closing_km
        })
        return redirect(url_for('add_vehicle'))
    
    return render_template('add_vehicle.html')

# Route for deleting an existing vehicle record
@app.route('/delete_vehicle', methods=['GET', 'POST'])
def delete_vehicle():
    if request.method == 'POST':
        vehicle_number = request.form['vehicle_number']
        
        result = collection.delete_one({"Vehicle Number": vehicle_number})
        if result.deleted_count > 0:
            return f"Vehicle {vehicle_number} deleted successfully."
        else:
            return f"Vehicle {vehicle_number} not found."
    
    return render_template('delete_vehicle.html')

if __name__ == '__main__':
    app.run(debug=True)
