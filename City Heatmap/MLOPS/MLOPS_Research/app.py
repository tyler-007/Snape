import streamlit as st
import pandas as pd
import numpy as np
from model_predict import *
import streamlit as st
import pandas as pd
import plotly.express as px
from Script_fetch_from_db import cursor_df as filtered_df
import math
import datetime



def main():
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
    map_object.update_layout(height=600, width=800)


    st.plotly_chart(map_object)

    adjustment_factors = {
    'Mon': 1.23,
    'Tue': 0.90,
    'Wed': 1.06,
    'Thur': 1.0,
    'Fri': 1.33,
    'Sat': 1.14,
    'Sun': 0.92
}

    regions = predicted_values
    
    cols = st.columns(len(regions))
    for i, (region, value) in enumerate(regions.items()):
        with cols[i]:
            day_of_week = datetime.datetime.now().strftime('%a')
            adjusted_value = value * adjustment_factors[day_of_week]
            rounded_value = round(abs(adjusted_value))

            st.button(str(rounded_value), key=f"btn_{region}")
            st.write(region)

   

if __name__ == "__main__":
    main()
