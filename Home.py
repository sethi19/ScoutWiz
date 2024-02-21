import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def app():
    

    ### Load Data ###
    model_results = pd.read_csv("/users/aayush/Desktop/FrontEnd/display_df1.csv")
    ZipAnchor = pd.read_csv("/users/aayush/Desktop/FrontEnd/zipAncho2.csv")
    Sampledf1 = pd.read_csv("/users/aayush/Desktop/SampleTable.csv")
    sampledf2 = Sampledf1.style.format({"Updated": '{:.0f}'})

    ### Sidebar ###
    filtering_method = st.sidebar.radio("Choose Filtering Method", ["Zip Code", "City/State"])

    if filtering_method == "Zip Code":
        selected_option = st.sidebar.text_input("Enter zipcodes, maximum 5 (comma-separated):")
        if st.sidebar.button("Randomize 5 Zips"):
            random_zips = list(np.random.choice(model_results['Zip Code'], size=5, replace=False))
            st.sidebar.text_input("5 randomized zipcodes", ", ".join(map(str, random_zips)))
            selected_option = ", ".join(map(str, random_zips))
        filtered_data = model_results[model_results['Zip Code'].isin(map(int, selected_option.split(', ')))] if selected_option else model_results
    else:
        selected_state = st.sidebar.selectbox("State", model_results['State'].unique())
        all_cities_for_state = model_results[model_results['State'] == selected_state]['City'].unique()
        cities_options = ["Select All"] + list(all_cities_for_state)
        selected_cities = st.sidebar.multiselect("City", cities_options)

        if "Select All" in selected_cities:
            selected_cities = all_cities_for_state

        filtered_data = model_results[(model_results['State'] == selected_state) & 
                                      (model_results['City'].isin(selected_cities))] if selected_state else model_results

    ### Main content area ###  
    st.title('Site Selection Webapp')
    st.write(" Using machine learning and location analytics, ScoutWize helps businesses predict the optimal zip code for their next venture – whether it's a restaurant, gas station, or retail store. Our consultancy will guide your strategic decisions, ensuring your business thrives in the right location. ")

    st.subheader('Model Results', divider='rainbow')
    
    expander = st.expander("Explore the data that powers the model")
    expander.write("""
        The following data sets were used to create this prediction model. *ScoutWize can use any data points related to your specific business needs.* 
    """)
    
    expander.dataframe(sampledf2, hide_index=True)

    
                     
                     
                     
    if not filtered_data.empty:
        styled_df = filtered_data[["Zip Code", "State", "City", "Orders Forecast", "Sales Forecast", "Decision"]].style.format({"Zip Code": '{:.0f}', "Orders Forecast": '{:,.2f}', "Sales Forecast": '{:,.2f}'})
        st.dataframe(styled_df, hide_index=True)
    else:
        st.write("No data found.")

    ### Map ###
    if not filtered_data.empty:
        fig_scatter_geo = px.scatter_geo(
            filtered_data,
            lat="latitude",
            lon="longitude",
            color="Sales Forecast",
            size="Sales Forecast",
            hover_name="Zip Code",
            custom_data=["Decision", "Orders Forecast", "Sales Forecast"],
            title="",
            scope="usa",
            size_max=10
        )

        fig_scatter_geo.update_layout(
            geo=dict(bgcolor='rgba(0,0,0,0)'),
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )

        fig_scatter_geo.update_traces(
            hovertemplate="<br>".join([
                "Zip Code: %{hovertext}",
                "Decision: %{customdata[1]}",
                "Orders Forecast: %{customdata[2]}",
                "Sales Forecast: %{customdata[3]:,.2f}"
            ])
        )

        fig_scatter_geo.update_traces(
            marker=dict(
                symbol='square',
                color=filtered_data['Sales Forecast'],
                colorscale='Blues',
                colorbar=dict(
                    title='Sales Forecast',
                    tickformat=',.2f',
                ),
            )
        )

        st.plotly_chart(fig_scatter_geo)
    else:
        st.warning("No data available for mapping.")

    ### Ball Tree Results ### 
    zipcodes = [int(str(zipcode).strip()) for zipcode in selected_option.split(', ') if str(zipcode).strip()] if filtering_method == "Zip Code" else [int(str(zipcode).strip()) for city in selected_cities for zipcode in model_results[model_results['City'] == city]['Zip Code'].unique() if str(zipcode).strip()]
    zip_anchor_columns = ['input', 'match 1', 'match 2', 'match 3', 'match 4']
    zip_anchor_row = ZipAnchor[ZipAnchor['input'].isin(zipcodes)]

    if not zip_anchor_row.empty:
        relevant_data_display_df2 = model_results[model_results['Zip Code'].isin(zip_anchor_row[zip_anchor_columns].values.flatten())]

        st.subheader('Find Similar Zip Codes', divider='rainbow')
        st.write("For each given zip code input, the model recommends four additional zip codes with similarities in demographic, economic, and industry-specific data points. This suggestion aims to provide a comprehensive understanding of comparable areas, aiding in strategic decision-making for businesses considering new locations. By leveraging data-driven insights, businesses can explore alternative zip codes that align with their specific criteria and preferences.")

        expander2 = st.expander("How do we find similar zip codes? ")
        expander2.write("""
        Based on your input, ScoutWize employs a ball tree model to match zip codes based on population, income, and housing prices. *The flexibility of ScoutWize allows customization of this model to align with specific business requirements.* 
        """)
            
        styled_df2 = zip_anchor_row[zip_anchor_columns].style.format({"input": '{:.0f}', "match 1": '{:.0f}', "match 2": '{:.0f}', "match 3": '{:.0f}', "match 4": '{:.0f}'})
        st.dataframe(styled_df2, hide_index=True)    

        st.write("Model predictions for Similar Zip Codes found")
        styled_df3 = relevant_data_display_df2[["Zip Code", "State", "City", "Orders Forecast", "Sales Forecast", "Decision"]].style.format({"Zip Code": '{:.0f}', "Orders Forecast": '{:,.2f}', "Sales Forecast": '{:,.2f}'})
        st.dataframe(styled_df3, hide_index=True)
    else:
        st.warning("No similar zip codes found.")

if __name__ == "__main__":
    app()
