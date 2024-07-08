from flask import Flask, request, jsonify
from pymongo import MongoClient

from urllib.parse import quote_plus
import certifi

ca_cert_bundle = certifi.where()  
username = 'bt22cse089'
password = 'aayush@123'
encoded_password = quote_plus(password)
connection_string = f'mongodb+srv://{username}:{encoded_password}@for-testing.ocsya6p.mongodb.net/?retryWrites=true&w=majority&appName=For-testing&tlsCAFile={ca_cert_bundle}'

# MongoDB connection
client = MongoClient(connection_string)
db = client["VehicleMaintenance"]
collection = db["VehicleReading"]

app = Flask(__name__)

# Add new vehicle endpoint
@app.route('/api/add_vehicle', methods=['POST'])
def add_vehicle():
    data = request.get_json()
    vehicle_number = data.get('vehicle_number')
    closing_km = data.get('closing_km')
    
    if vehicle_number and closing_km is not None:
        try:
            collection.insert_one({
                "Vehicle Number": vehicle_number,
                "Closing KM": closing_km,
                "current_reading": closing_km
            })
            return jsonify({"message": f"Vehicle {vehicle_number} added successfully."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid data provided."}), 400

# Delete vehicle endpoint
@app.route('/api/delete_vehicle/<vehicle_number>', methods=['DELETE'])
def delete_vehicle(vehicle_number):
    try:
        result = collection.delete_one({"Vehicle Number": vehicle_number})
        if result.deleted_count > 0:
            return jsonify({"message": f"Vehicle {vehicle_number} deleted successfully."}), 200
        else:
            return jsonify({"error": f"Vehicle {vehicle_number} not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
