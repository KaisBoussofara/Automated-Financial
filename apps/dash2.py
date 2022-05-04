import plost as plost
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf
import plotly_express as px

def app():
    st.title('Finance Dashbord')
    tickers = ('TSLA','AAPL','MSFT','BTC-USD','ETH-USD')
    dropdown = st.multiselect('Pick your assets', tickers)
    start = st.date_input('Start',value=pd.to_datetime('2022-01-01'))
    end = st.date_input('End',value=pd.to_datetime('today'))
    if len(dropdown)>0 :
        df = yf.download(dropdown,start,end)['Adj Close']
        st.line_chart(df)
