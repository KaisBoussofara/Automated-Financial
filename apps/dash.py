import plost as plost
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import plotly_express as px
import numpy





def LoadData(fin):
    data = pd.read_csv(fin, skiprows=1)
    return data

def LoadData2(fin):
    data = pd.read_csv(fin,index_col=0,header=0)
    return data
def LoadData3(fin):
    data = pd.read_csv(fin)
    return data

def Tcsv1(fnin, fnout):
    fin = open(fnin, "r")
    fout = open(fnout, "w")
    for line in numpy.array([s.strip('\n').split(',') for s in fin]).T:
        fout.write(",".join(line) + "\n")
    fin.close()
    fout.close()

def TransposeINS(fin,row):
    data = pd.read_csv(fin)
    data= data.iloc[[row],[2,3,4,5,6]]
    df=pd.DataFrame(data)
    df.to_csv('In.csv')
    Tcsv1('In.csv','out.csv')

def TransposeBC(fin,row):
    data = pd.read_csv(fin)
    data= data.iloc[[row],[2,3,4]]
    df=pd.DataFrame(data)
    df.to_csv('In.csv')
    Tcsv1('In.csv','out.csv')

def highlight_cols(s):
    return 'background-color: % s' % 'yellow'

def app():
    option = st.selectbox(
        'Pick your assets',
        ('CEG','ANSS','ETR','GE','HST'))
    col1,col2 = st.columns([3,1])
    col11, col12,col13 = st.columns(3)
    #Data=LoadData(f'~/PycharmProjects/pythonProject1/04. {option} Stock Price - 5 Year Historical.csv')
    df = LoadData2(f'~/PycharmProjects/pythonProject1/06.{option} Piotroski Score Results.csv')
    df2 = LoadData3(f'~/PycharmProjects/pythonProject1/01. {option} Income Statement.csv')
    df3=LoadData3(f'~/PycharmProjects/pythonProject1/02. {option} Balance Sheet.csv')
    #stock_plot.show()
    with st.container():
        with col1:
            st.header(f'{option} Stock Open Prices')
            #stock_plot = px.line(x='Date', y='Open', data_frame=Data,width=1200)
            #fig = stock_plot.update_traces(line_color='lightgreen')
            #st.plotly_chart(fig)

            ################
        with col2:
            st.header(f'{option} Scoring Criteria')
            st.dataframe(df.style.highlight_max(color='lightgreen').applymap(highlight_cols, subset = df.iloc[2,1]),width=600,height=1500)
            #st.write(df.style.highlight_max(color='lightgreen').applymap(highlight_cols, subset = df.iloc[2,1]),height=15500)
    with st.container():
        with col11 :
            TransposeBC(f'~/PycharmProjects/pythonProject1/02. {option} Balance Sheet.csv',1)
            data = pd.read_csv('out.csv')
            data.columns = ["Year", "Total Assets"]
            df = pd.DataFrame(data)
            df.iat[0, df.columns.get_loc('Year')] = '12/31/2022'
            fig = px.bar(df, x='Year', y='Total Assets',width=500,title="Total Assets",)
            st.subheader(f'{option}- Total Assets')
            fig =fig.update_traces(marker_color='lightgreen')
            st.plotly_chart(fig)
        with col12:

            TransposeBC(f'~/PycharmProjects/pythonProject1/02. {option} Balance Sheet.csv', 9)
            data = pd.read_csv('out.csv')
            data.columns = ["Year", "Total Debt"]
            df = pd.DataFrame(data)
            df.iat[0, df.columns.get_loc('Year')] = '12/31/2022'
            fig = px.bar(df, x='Year', y='Total Debt', width=500, title="Total Debt", )
            st.subheader(f'{option}- Total Debt')
            fig = fig.update_traces(marker_color='Red')
            st.plotly_chart(fig)
        with col13:
            TransposeINS(f'~/PycharmProjects/pythonProject1/01. {option} Income Statement.csv', 1)
            data = pd.read_csv('out.csv')
            data.columns = ["Year", "Total Equity"]
            df = pd.DataFrame(data)
            df.iat[0, df.columns.get_loc('Year')] = '12/31/2022'
            fig = px.bar(df, x='Year', y='Total Equity', width=500, title="Total Equity" )
            st.subheader(f'{option} Total Equity')
            fig = fig.update_traces(marker_color='lightgreen')
            st.plotly_chart(fig)
    with st.container():
        with col11:
            TransposeINS(f'~/PycharmProjects/pythonProject1/01. {option} Income Statement.csv', 1)
            data = pd.read_csv('out.csv')
            data.columns = ["Year", "Total Revenue"]
            df = pd.DataFrame(data)
            df.iat[0, df.columns.get_loc('Year')] = '12/31/2022'
            st.subheader(f'{option}- Revenue')
            stock_plot = px.line(x='Year', y='Total Revenue', data_frame=df,width=500)
            fig = stock_plot.update_traces(line_color='lightgreen')
            st.plotly_chart(fig)
        with col12:
            TransposeINS(f'~/PycharmProjects/pythonProject1/01. {option} Income Statement.csv', 16)
            data = pd.read_csv('out.csv')
            data.columns = ["Year", "Total Expanses"]
            df = pd.DataFrame(data)
            df.iat[0, df.columns.get_loc('Year')] = '12/31/2022'
            st.subheader(f'{option} Total Expanses')
            stock_plot = px.line(x='Year', y='Total Expanses', data_frame=df,width=500)
            fig = stock_plot.update_traces(line_color='Red')
            st.plotly_chart(fig)
        with col13:
            TransposeINS(f'~/PycharmProjects/pythonProject1/01. {option} Income Statement.csv', 10)
            data = pd.read_csv('out.csv')
            data.columns = ["Year", "Net Income "]
            df = pd.DataFrame(data)
            df.iat[0, df.columns.get_loc('Year')] = '12/31/2022'
            st.subheader(f'{option}- Net Income')
            stock_plot = px.line(x='Year', y='Net Income ', data_frame=df,width=500)
            fig = stock_plot.update_traces(line_color='lightgreen')
            st.plotly_chart(fig)
