
# Define your hourly demand data for the 6 zones
hourly_demand = {
    'Kolkata City': 400,
    'Howrah': 78,
    'Airport': 20,
    'Dakshindari': 60,
    'SectorV': 90,
    'Victoria': 20
}
'''
# Define the function to create the circle button
def create_circle_button(zone, demand):
    return st.button(f'{demand}', key=zone, help=zone)

# Create the two columns for the two lines
col1, col2 = st.columns(2)

# First line with 3 zones
with col1:
    create_circle_button('Kolkata City', hourly_demand['Kolkata City'])
    st.markdown('<p style="text-align: center;">Kolkata City</p>', unsafe_allow_html=True)
    create_circle_button('Howrah', hourly_demand['Howrah'])
    st.markdown('<p style="text-align: center;">Howrah</p>', unsafe_allow_html=True)
    create_circle_button('Airport', hourly_demand['Airport'])
    st.markdown('<p style="text-align: center;">Airport</p>', unsafe_allow_html=True)

# Second line with 3 zones
with col2:
    create_circle_button('Dakshindari', hourly_demand['Dakshindari'])
    st.markdown('<p style="text-align: center;">DakshinDari</p>', unsafe_allow_html=True)
    create_circle_button('SectorV', hourly_demand['SectorV'])
    st.markdown('<p style="text-align: center;">SectorV</p>', unsafe_allow_html=True)
    create_circle_button('Victoria', hourly_demand['Victoria'])
    st.markdown('<p style="text-align: center;">Victoria Memorial</p>', unsafe_allow_html=True)

    '''