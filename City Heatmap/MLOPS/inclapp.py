import streamlit as st
import pandas as pd
import numpy as np
from model_predict import *
from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import plotly.express as px
from Script_fetch_from_db import cursor_df as filtered_df
import math
import folium
from streamlit_folium import folium_static
import datetime
from datetime import timedelta


adjustment_factors = {
        'Mon': 1.23,
        'Tue': 0.90,
        'Wed': 1.06,
        'Thu': 1.0,
        'Fri': 1.33,
        'Sat': 1.14,
        'Sun': 0.92
    }

now =datetime.datetime.now()

now = now + timedelta(hours=5, minutes=30)
now_1=now + timedelta(hours=1)

hour_12 = now.strftime('%I %p')  
hour_13=now_1.strftime('%I %p')

def create_predicted_values_map():
    locations = {
        "dakshindari": (22.610619, 88.409662),
        "sectorV": (22.576222, 88.435053),
        "victoria": (22.552652, 88.352503),
        "howrah": (22.583474, 88.342969),
        "airport": (22.642434, 88.439351)
    }
    

    # Create a map centered around the mean of all locations
    map_center = [sum([loc[0] for loc in locations.values()]) / len(locations),
                  sum([loc[1] for loc in locations.values()]) / len(locations)]
    mymap = folium.Map(location=map_center, zoom_start=12)

    for name, coord in locations.items():
        predicted_value = predicted_values.get(name, 0)  
        
        day_of_week = datetime.datetime.now().strftime('%a')
        adjusted_value = predicted_value * adjustment_factors.get(day_of_week, 1.0)
        rounded_value = round(abs(adjusted_value))
        popup_text = f"{name}: Predictions - {rounded_value}"

        radius = math.sqrt(rounded_value) * 4
        
        folium.CircleMarker(
            location=coord,
            radius=radius,
            popup=popup_text,
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(mymap)

    return mymap


   


def main():
    logo_path = "snape_logo.png"
    st.logo(logo_path)
    if 'visit_count' not in st.session_state:
        st.session_state['visit_count'] = 0
    st.session_state['visit_count'] += 1
    st.sidebar.write(f"Visit count: {st.session_state['visit_count']}")
    st.title("Heatmap and hourly prediction- SNAPE")
    st.subheader("Unique requests heatmap - past 25 hours")
    map_object = px.density_mapbox(
        filtered_df,
        lat="latitude",
        lon="longitude",
        radius=15,
        center=dict(lat=filtered_df['latitude'].mean(), lon=filtered_df['longitude'].mean()),
        zoom=10,
        mapbox_style="open-street-map",
        range_color=(25, 125),  
        color_continuous_scale="viridis" 
    )

    map_object.update_traces(
        colorbar=dict(
            title="Density",
            titleside="top",
            tickmode="array",
            tickvals=[25, 50, 75, 100, 125],
            ticktext=["Low", "25%", "50%", "75%", "High"]
        )
    )
    map_object.update_layout(height=600, width=1800)


    st.plotly_chart(map_object)
    
    st.subheader(f"Predictions for {hour_12} - {hour_13}")

    regions = predicted_values
    
    cols = st.columns(len(regions))
    for i, (region, value) in enumerate(regions.items()):
        with cols[i]:
            day_of_week = datetime.datetime.now().strftime('%a')
            adjusted_value = value * adjustment_factors[day_of_week]
            rounded_value = round(abs(adjusted_value))

            st.button(str(rounded_value), key=f"btn_{region}")
            
            st.write(region)



    st.subheader('Predicted Values for next hour on map')
    predicted_values_map = create_predicted_values_map()
    folium_static(predicted_values_map)




if __name__ == "__main__":
    main()
