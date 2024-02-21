import streamlit as st
from streamlit_option_menu import option_menu
import Home, Explore

st.set_page_config(
    page_title="ScoutWize",
    page_icon=":globe_with_meridians:",
    layout="wide",
    initial_sidebar_state="expanded",
)


class MultiApp:
    
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title='ScoutWize ',
                options=['Home', 'Explore'],
                icons=['house-fill', 'graph-up-arrow'],
                menu_icon='globe2',
                default_index=0,  # Fix: Set default_index to 0
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "18px"},
                    "nav-link": {"color": "white", "font-size": "15px", "text-align": "left", "margin": "0px",
                                 "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )
            
            st.markdown('<a href="https://scoutwize.com" target="_blank">Visit our Website!</a>', unsafe_allow_html=True)

        if app == "Home":
            Home.app()
        
        if app == "Explore":
            Explore.app()
            

if __name__ == '__main__':
    MultiApp().run()
