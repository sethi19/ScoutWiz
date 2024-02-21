import streamlit as st 
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px


def app():
    # Load the data
    model_results = pd.read_csv("/users/aayush/Desktop/df2.csv")
    # Option for choosing filtering method
    filtering_method = st.sidebar.radio("Choose Filtering Method", ["Zip Code", "City/State"])

    # Filtering based on user input
    if filtering_method == "Zip Code":
        selected_option = st.sidebar.text_input("Enter zipcodes, maximum 5 (comma-separated):")
        if st.sidebar.button("Randomize 5 Zips"):
            random_zips = list(np.random.choice(model_results['Zip Code'], size=5, replace=False))
            st.sidebar.text_input("5 randomized zipcodes", ", ".join(map(str, random_zips)))
            selected_option = ", ".join(map(str, random_zips)) 
        # Filter the data based on zip code
        filtered_data = model_results[model_results['Zip Code'].isin(map(int, selected_option.split(', ')))] if selected_option else model_results
    else:
        selected_state = st.sidebar.selectbox("State", model_results['State'].unique())
        
        # Create a list with "Select All" option followed by all cities for the chosen state
        all_cities_for_state = model_results[model_results['State'] == selected_state]['City'].unique()
        cities_options = ["Select All"] + list(all_cities_for_state)
        
        # Allow the user to choose multiple cities using a multiselect dropdown
        selected_cities = st.sidebar.multiselect("City", cities_options)
        
        # If "Select All" is chosen, consider all cities for filtering
        if "Select All" in selected_cities:
            selected_cities = all_cities_for_state
        
        # Filter the data based on city/state
        filtered_data = model_results[(model_results['State'] == selected_state) & 
                                    (model_results['City'].isin(selected_cities))] if selected_state else model_results




### MAIN PAGE  ######----------------------------------
    st.subheader('Custom Dashboard', divider='rainbow')
    st.write("We can create a custom dashboard based on your business needs. ")
    top_20_orders = filtered_data.sort_values(by='Orders', ascending=False)
    top_20_sales = filtered_data.sort_values(by='Sales', ascending=False)

    chart1 = alt.Chart(top_20_orders).mark_bar().encode(
    x=alt.X('Zip Code:N', title='Zip Code', sort='-y'),
    y=alt.Y('Orders:Q', title='Orders'),
        ).properties(width=350, height=200,title='Orders by Zip Code')

# Altair Chart for Sales
    chart2 = alt.Chart(top_20_sales).mark_bar().encode(
    x=alt.X('Zip Code:N', title='Zip Code', sort='-y'),
    y=alt.Y('Sales:Q', title='Sales'),
        ).properties(width=350, height=200, title='Sales by Zip Code')

#   Display Altair charts side by side
    st.altair_chart(chart1 | chart2)
    
    
    
    StateDF = model_results.groupby("State")[["Sales", "Orders"]].sum().reset_index()
    # selected_state = st.multiselect("Select State:", ["All"] + list(StateDF['State'].unique()))

    # Display the filter for State (multi-select)
    selected_states = st.multiselect("Select State(s):", ["All"] + list(StateDF['State'].unique()))

    # Filter the data based on the selected state(s)
    if "All" not in selected_states:
        StateDF = StateDF[StateDF['State'].isin(selected_states)]
        
    
    chart3 = alt.Chart(StateDF).mark_bar().encode(
    x=alt.X('State:N', title='', sort='-y'),
    y=alt.Y('Sales:Q', title='Sales'),
        ).properties(width=350, height=200, title='Sales by State')
    
    chart4 = alt.Chart(StateDF).mark_bar().encode(
    x=alt.X('State:N', title='', sort='-y'),
    y=alt.Y('Orders:Q', title='Orders'),
        ).properties(width=350, height=200, title='Orders by State')

    
    st.altair_chart(chart3 | chart4)
    
    
    
    
    def generate_fake_data():
        # Generate fake data for demonstration
        states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado"]
        years = list(range(2017, 2025))

        data = {
            "State": np.random.choice(states, size=100),
            "Year": np.random.choice(years, size=100),
            "Sales": np.random.uniform(100, 1000, size=100),
            "Orders": np.random.uniform(50, 500, size=100),
        }
        return pd.DataFrame(data)

    # Generate fake data
    model_results2 = generate_fake_data()

    # Group by State and Year, sum Sales and Orders
    StateDF2 = model_results2.groupby(["State", "Year"])[["Sales", "Orders"]].sum().reset_index()

    # Display the filter for State (multi-select)
    selected_states2 = st.multiselect("Select State(s):", ["All"] + list(StateDF2['State'].unique()))

    # Filter the data based on the selected state(s)
    if "All" not in selected_states2:
        StateDF2 = StateDF2[StateDF2['State'].isin(selected_states2)]

    # Create Altair charts for Sales and Orders
    chart5 = alt.Chart(StateDF2).mark_line().encode(
        x=alt.X('Year:N', title='Year'),
        y=alt.Y('Sales:Q', title='Sales'),
        color='State:N',
    ).properties(width=350, height=200, title='Sales by State')

    chart6 = alt.Chart(StateDF2).mark_line().encode(
        x=alt.X('Year:N', title='Year'),
        y=alt.Y('Orders:Q', title='Orders'),
        color='State:N',
    ).properties(width=350, height=200, title='Orders by State')

    # Display the charts side by side
    st.altair_chart(chart5 | chart6)
    
    
    
    
    
    

    
    
    
    

if __name__ == "__main__":
    app()
