import streamlit as st
from multiapp import MultiApp
from apps import app , dash , dash2

appli = MultiApp()
st.set_page_config(page_title="Financial analysis",layout="wide")
st.markdown('Finance Dashbord')

appli.add_app("Dashbord",dash.app)
appli.add_app("2nd Dashbord",dash2.app)
appli.add_app("3rd Dashbord",app.app)
appli.run()