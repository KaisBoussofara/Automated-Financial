import pyrebase
import streamlit as st
from datetime import datetime


firebaseConfig = {

  'apiKey': "AIzaSyCzg_coaz61SwUvvWVKyX_WYfJc8gUx1_U",

  'authDomain': "financal-analysis.firebaseapp.com",

  'projectId': "financal-analysis",

  'storageBucket': "financal-analysis.appspot.com",

  'messagingSenderId': "386608344074",

  'appId': "1:386608344074:web:070702b88bffdef11783f3",

  'databaseURL' : "https://financal-analysis-default-rtdb.europe-west1.firebasedatabase.app/",

  'measurementId': "G-XZFKW2SGQN"

}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()
