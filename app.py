import streamlit as st
from multiapp import MultiApp
from apps import app , dash , dash2,dash3

import pickle
from pathlib import Path
import streamlit_authenticator as stauth


appli = MultiApp()
st.set_page_config(page_title="Financial analysis",layout="wide")
#st.markdown('Finance Dashboard')

names = ["Peter Parker", "Rebecca Miller"]
usernames = ["pparker", "rmiller"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords
                                    ,"sales_dashboard", "abcdef") #,cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    st.session_state['authenticator']=authenticator
    appli.add_app("Income Statement", dash.app)
    #appli.add_app("2nd Dashboard", dash2.app)
    appli.add_app("S&P 500 Stock closing price", app.app)
    appli.add_app("Sentimental Analysis Compound Score", dash3.app)
    appli.run()
