import plost as plost
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf
import plotly_express as px
import csv

import sys
import numpy
def csvt_1(fnin, fnout):
    fin = open(fnin, "r")
    fout = open(fnout, "w")
    for line in numpy.array([s.strip('\n').split(',') for s in fin]).T:
        fout.write(",".join(line) + "\n")
    fin.close()
    fout.close()

data = pd.read_csv('~/PycharmProjects/pythonProject1/01. CEG Income Statement.csv')
data= data.iloc[[1],[2,3,4,5,6]]
df=pd.DataFrame(data)
df.to_csv('In.csv')
csvt_1('In.csv','out.csv')
data = pd.read_csv('out.csv')
data.columns = ["Year", "Income" ]
df=pd.DataFrame(data)
df.iat[0, df.columns.get_loc('Year')] = '12/31/2022'
fig = px.bar(df,x='Year',y='Income')
fig.show()
