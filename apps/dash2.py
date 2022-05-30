import pandas as pd
import streamlit as st
import yfinance as yf


def app():
    st.title('Finance Dashbord')
    tickers = ('TSLA','AAPL','MSFT','BTC-USD','ETH-USD')
    dropdown = st.multiselect('Pick your assets', tickers)
    start = st.date_input('Start',value=pd.to_datetime('2022-01-01'))
    end = st.date_input('End',value=pd.to_datetime('today'))
    if len(dropdown)>0 :
        df = yf.download(dropdown,start,end)['Adj Close']
        st.line_chart(df)
