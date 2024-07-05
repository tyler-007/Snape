import streamlit as st
import folium
import math
import datetime
from streamlit_folium import folium_static

def create_predicted_values_map():
    # Coordinates for the locations
    locations = {
        "Dakshindari": (22.610619, 88.409662),
        "Sector 5": (22.576222, 88.435053),
        "Victoria Memorial": (22.552652, 88.352503),
        "Howrah": (22.583474, 88.342969),
        "Airport": (22.642434, 88.439351)
    }

    # Example predicted values (replace this with your actual predicted values)
    predicted_values = {
        "Dakshindari": 10,
        "Sector 5": 20,
        "Victoria Memorial": 30,
        "Howrah": 40,
        "Airport": 50
    }

    # Adjustment factors based on the day of the week
    adjustment_factors = {
        'Mon': 1.23,
        'Tue': 0.90,
        'Wed': 1.06,
        'Thur': 1.0,
        'Fri': 1.33,
        'Sat': 1.14,
        'Sun': 0.92
    }

    # Create a map centered around the mean of all locations
    map_center = [sum([loc[0] for loc in locations.values()]) / len(locations),
                  sum([loc[1] for loc in locations.values()]) / len(locations)]
    mymap = folium.Map(location=map_center, zoom_start=12)

    # Plot the locations with circular markers
    for name, coord in locations.items():
        # Get the predicted value for this location
        predicted_value = predicted_values.get(name, 0)  # Default to 0 if not found
        
        # Calculate adjusted value based on current day of the week
        day_of_week = datetime.datetime.now().strftime('%a')
        adjusted_value = predicted_value * adjustment_factors.get(day_of_week, 1.0)
        rounded_value = round(abs(adjusted_value))

        # Create popup text
        popup_text = f"{name}: Predictions - {rounded_value}"

        # Calculate radius based on the adjusted value (scaling factor may need adjustment)
        radius = math.sqrt(rounded_value) * 10
        
        # Add circle marker to map
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
    st.title('Predicted Values Map')
    
    # Generate Folium map with predicted values
    predicted_values_map = create_predicted_values_map()
    
    # Display Folium map in Streamlit app
    folium_static(predicted_values_map)

if __name__ == "__main__":
    main()
