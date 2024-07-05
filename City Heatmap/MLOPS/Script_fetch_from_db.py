import pandas as pd
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime, timedelta

import certifi

ca_cert_bundle = certifi.where()  # Use the system's trusted CA bundle


username = 'ML_Snape'
password = 'Learn@2024'
encoded_password = quote_plus(password)
connection_string = f'mongodb+srv://{username}:{encoded_password}@snapeeapp.3rtq6.mongodb.net/?retryWrites=true&w=majority&appName=snapeeApp&tlsCAFile={ca_cert_bundle}'


'''
connection_string=f'mongodb+srv://ML_Snape:Learn@2024@snapeeapp.3rtq6.mongodb.net/?retryWrites=true&w=majority&appName=snapeeApp&tlsCAFile={ca_cert_bundle}'
'''


client = MongoClient(connection_string)
db = client['snapee']
collection = db['bookings_rides']

current_datetime = datetime.now()
current_datetime_utc = current_datetime -timedelta(hours=5,minutes=30)
prev_25_hours_utc = current_datetime_utc - timedelta(hours=26)

# Query and projection
query = {
    'createdDate': {
        '$gte': prev_25_hours_utc,
        '$lte': current_datetime_utc
    }
}
projection = {
    'createdDate': 1,
    'pickup.location.latitude': 1,
    'pickup.location.longitude': 1,
    'bookingDateDevice': 1,
    'createdBy.mobile': 1,
    'bookingDateDevice': 1
}

# Execute the query and fetch the data
cursor = collection.find(query, projection)
cursor_list = list(cursor)

# Check if cursor_list is not empty
if cursor_list:
    # Convert the cursor to a pandas DataFrame
    cursor_df = pd.DataFrame(cursor_list)
    cursor_df['longitude'] = cursor_df['pickup'].apply(lambda x: x['location']['longitude'])
    cursor_df['latitude'] = cursor_df['pickup'].apply(lambda x: x['location']['latitude'])
    cursor_df['createdBy.mobile'] = cursor_df['createdBy'].apply(lambda x: str(x['mobile']))
    cursor_df = cursor_df.drop(['pickup', 'createdBy'], axis=1)
    print(cursor_df)
else:
    print("No data found.")

# Close the MongoDB client connection
client.close()

#

'''import pandas as pd
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime, timedelta
username = 'bt22cse089'
password = 'aayush@123'
encoded_password = quote_plus(password)

connection_string = f'mongodb+srv://{username}:{encoded_password}@for-testing.ocsya6p.mongodb.net/?retryWrites=true&w=majority&appName=For-testing'

client = MongoClient(connection_string)
db = client['newdb']
collection = db['newAppCollection']

print("connection Done")
current_datetime = datetime.now()
current_datetime_utc = current_datetime - timedelta(hours=5, minutes=30)
prev_25_hours_utc= current_datetime_utc - timedelta(hours=25)

query = {
    'createdDate': {
        '$gte': prev_25_hours_utc,
        '$lte': current_datetime_utc
    }
}

# Projection to select specific fields
projection = {
    'bookingId': 1,
    'pickup.location.latitude': 1,
    'pickup.location.longitude': 1,
    'bookingDateDevice': 1,
    'createdBy.mobile': 1,
    'bookingDateDevice':1
}

try:
    cursor = collection.find(query, projection)
    print("fetch done")
    print(cursor)
except Exception as e:
    print(f"An error occurred while fetching data: {e}")


try:
    cursor = collection.find(query, projection)
    print("fetch done")
    cursor_list = list(cursor)
    if cursor_list:  
        cursor_df = pd.DataFrame(cursor_list)  
        print(cursor_df)
    else:
        print("Cursor is empty.")
except Exception as e:
    print(f"An error occurred while fetching data: {e}")




import pandas as pd
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime, timedelta

import certifi

ca_cert_bundle = certifi.where()  # Use the system's trusted CA bundle


username = 'snapee_user'
password = 'w3O3Fjlk5wsvnUt9'
encoded_password = quote_plus(password)
connection_string = f'mongodb+srv://{username}:{encoded_password}@snapeeapp.3rtq6.mongodb.net/?retryWrites=true&w=majority&appName=snapeeApp&tlsCAFile={ca_cert_bundle}'
# Connect to MongoDB
client = MongoClient(connection_string)
db = client['SnapeeApp']
collection = db['booking_rides']

# Current datetime and time range for query
current_datetime = datetime.now()
current_datetime_utc = current_datetime - timedelta(hours=5, minutes=30)
prev_25_hours_utc = current_datetime_utc - timedelta(hours=25)

# Query and projection
query = {
    'createdDate': {
        '$gte': prev_25_hours_utc,
        '$lte': current_datetime_utc
    }
}
projection = {
    'bookingId': 1,
    'pickup.location.latitude': 1,
    'pickup.location.longitude': 1,
    'bookingDateDevice': 1,
    'createdBy.mobile': 1,
    'bookingDateDevice': 1
}

try:
    # Execute the query and fetch the data
    cursor = collection.find(query, projection)
    cursor_list = list(cursor)

    # Convert the cursor to a pandas DataFrame
    if cursor_list:
        cursor_df = pd.DataFrame(cursor_list)
        cursor_df['longitude'] = cursor_df['pickup'].apply(lambda x: x['location']['longitude'])
        cursor_df['latitude'] = cursor_df['pickup'].apply(lambda x: x['location']['latitude'])

        cursor_df['createdBy.mobile'] = cursor_df['createdBy'].apply(lambda x: str(x['mobile']))

        cursor_df = cursor_df.drop(['pickup', 'createdBy'], axis=1)
        print(cursor_df)
    else:
        print("No data found.")

except Exception as e:
    print(f"An error occurred while fetching data: {e}")

finally:
    client.close()

'''