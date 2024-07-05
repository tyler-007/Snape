import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
import certifi
from urllib.parse import quote_plus
import base64

# Certifi certificate
ca_cert_bundle = certifi.where()

# MongoDB credentials and URI
username = 'LSTM_Permission'
password = 'qiTsKeRRJbnlyEaY'
encoded_password = quote_plus(password)

# Corrected MongoDB URI
MONGO_URI = f'mongodb+srv://{username}:{encoded_password}@devsnapeeapp.3rtq6.mongodb.net/?retryWrites=true&w=majority&appName=devSnapeeApp&tlsCAFile={ca_cert_bundle}'
DATABASE_NAME = 'LSTM_store'

def get_mongo_collection(region):
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection_name = f"hourly{region}"
    collection = db[collection_name]
    return collection

def fetch_top_records(region, limit):
    collection = get_mongo_collection(region)
    cursor = collection.find().sort('_id', -1).limit(limit)
    data = list(cursor)
    df = pd.DataFrame(data)
    return df

def plot_hourly_data(df):
    df['hour_of_day'] = (df['hour_of_day'].astype(int)+23)%24
    grouped_df = df.groupby('hour_of_day')['y_lag_1'].sum().reset_index()

    fig = px.bar(grouped_df, x='hour_of_day', y='y_lag_1', title='Sum of Requests by Hour of Day')
    fig.update_xaxes(title_text='Hour of Day')
    fig.update_yaxes(title_text='Sum of Requests')
    return fig

def main():
    logo_path = "snape_logo.png"
    st.logo(logo_path)
    st.title("Hourly Data Visualization")

    regions = ["Airport", "City", "Dakshindari", "Howrah", "SectorV", "Victoria"]
    region = st.selectbox("Select Region:", options=regions)

    record_limits = [24, 72, 168, 720]
    record_limit = st.selectbox("Select Number of Records to Fetch:", options=record_limits, index=2)

    if st.button("Fetch Data"):
        with st.spinner('Fetching data...'):
            df = fetch_top_records(region, record_limit)
            if not df.empty:
                fig = plot_hourly_data(df)
                st.plotly_chart(fig)
                
                csv_download_link = get_csv_download_link(df, "hourly_data.csv")
                st.markdown(csv_download_link, unsafe_allow_html=True)
            else:
                st.write("No data found for the selected region.")

def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV file</a>'
    return href

if __name__ == "__main__":
    main()
