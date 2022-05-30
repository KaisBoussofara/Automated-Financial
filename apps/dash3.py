import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf
import plotly_express as px
import numpy
def LoadData3(fin):
    return pd.read_csv(fin,skiprows=0,usecols=[4,5])
def app():
    option = st.selectbox(
        'Pick your assets',
        ('ANSS', 'GE', 'ETR', 'CEG', 'HST'))
    col1, col2, col3 = st.columns([1, 6, 1])
    data = LoadData3(f'07.{option} Sentiment Analysis.csv')
    with st.container():
        with col2 :
            st.image(f'08.{option} Compound Score.png',width=1200)

    with st.container():
        with col2:
            st.title(f'{option} news article headings')
        with col2:
            st.dataframe(data)
