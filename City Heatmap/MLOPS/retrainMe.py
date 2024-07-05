import pandas as pd
from pymongo import MongoClient
from urllib.parse import quote_plus
import certifi
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import joblib


# MongoDB connection string
username = 'bt22cse089'
password = 'aayush@123'
encoded_password = quote_plus(password)
ca_cert_bundle = certifi.where()
connection_string = f'mongodb+srv://{username}:{encoded_password}@for-testing.ocsya6p.mongodb.net/?retryWrites=true&w=majority&appName=For-testing&tlsCAFile={ca_cert_bundle}'
# Connect to MongoDB
client = MongoClient(connection_string)
db = client['LSTM_store']

def fetch_from_mongodb(collection_name):
    collection = db[collection_name]
    data = list(collection.find({}))  
    return pd.DataFrame(data)

# Fetch data from each collection
hourly_demand_df = fetch_from_mongodb('hourlyDemand')
hourly_demand_airport_df = fetch_from_mongodb('hourlyAirport')
hourly_demand_dakshinDari_df = fetch_from_mongodb('hourlyDakshinDari')
hourly_demand_howrah_df = fetch_from_mongodb('hourlyHowrah')
hourly_demand_victoria_df = fetch_from_mongodb('hourlyVictoria')
hourly_demand_sectorV_df = fetch_from_mongodb('hourlySectorV')


def retrain(data,name):
    data['y'] = data['y_lag_1'].shift(1)
    data=data[['y','rain_intensity','rain_accumulation','temperature','hour_of_day','y_lag_1','y_lag_2','y_lag_10','y_lag_12','y_lag_14','y_lag_23','y_lag_24','y_lag_25']]

    data.dropna(inplace=True)
    train_data = data.iloc[:-50]
    test_data = data.iloc[-50:]

    X_train_raw = train_data.drop('y', axis=1).values
    y_train_raw = train_data['y'].values.reshape(-1, 1)
    X_test_raw = test_data.drop('y', axis=1).values
    y_test_raw = test_data['y'].values.reshape(-1, 1)

    # Scale features and target separately
    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()

    X_train_scaled = scaler_X.fit_transform(X_train_raw)
    y_train_scaled = scaler_y.fit_transform(y_train_raw)
    X_test_scaled = scaler_X.transform(X_test_raw)
    y_test_scaled = scaler_y.transform(y_test_raw)

    # Create sequences for the LSTM model
    TIME_STEPS = 1
    N_FEATURES = X_train_scaled.shape[1]

    def create_sequences(X, y, time_steps=TIME_STEPS):
        Xs, ys = [], []
        for i in range(len(X) - time_steps):
            Xs.append(X[i:i+time_steps])
            ys.append(y[i+time_steps])
        return np.array(Xs), np.array(ys)

    X_train, y_train = create_sequences(X_train_scaled, y_train_scaled)
    X_test, y_test = create_sequences(X_test_scaled, y_test_scaled)

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(128, input_shape=(TIME_STEPS, N_FEATURES), return_sequences=True))
    model.add(LSTM(32))
    model.add(Dropout(0.5))
    model.add(Dense(1))

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))

    # Make predictions on test data
    y_pred_scaled = model.predict(X_test)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)

    print("Predicted values:", y_pred)
    print("Actual values:", scaler_y.inverse_transform(y_test))

    joblib.dump(scaler_X, f'scaler_x_{name}.pkl')
    joblib.dump(scaler_y, f'scaler_y_{name}.pkl')
    model.save(f'lstm_{name}.h5')



retrain(hourly_demand_df,'kolkata_city')
retrain(hourly_demand_airport_df,'airport')
retrain(hourly_demand_dakshinDari_df,'dakshindari')
retrain(hourly_demand_howrah_df,'howrah')
retrain(hourly_demand_victoria_df,'victoria')
retrain(hourly_demand_sectorV_df,'sectorV')