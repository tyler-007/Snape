import streamlit as st
from inclapp import main as inclapp_main
from charts import main as charts_main

def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.selectbox('Select a page', ['Prediction', 'Charts'])

    if page == 'Prediction':
        inclapp_main()
    elif page == 'Charts':
        charts_main()

if __name__ == "__main__":
    main()
