import numpy
import pandas as pd
import plotly_express as px
import streamlit as st


def LoadData():
    data = pd.read_csv('~/PycharmProjects/pythonProject1/04. CEG Stock Price - 5 Year Historical.csv', skiprows=1)
    return data


def LoadData2():
    data = pd.read_csv('~/PycharmProjects/pythonProject1/06.CEG Piotroski Score Results.csv', index_col=0, header=0)
    return data


def LoadData3():
    data = pd.read_csv('~/PycharmProjects/pythonProject1/01. CEG Income Statement.csv')

    return data

def Tcsv1(fnin, fnout):
    fin = open(fnin, "r")
    fout = open(fnout, "w")
    for line in numpy.array([s.strip('\n').split(',') for s in fin]).T:
        fout.write(",".join(line) + "\n")
    fin.close()
    fout.close()

def Transpose():
    data = pd.read_csv('~/PycharmProjects/pythonProject1/01. CEG Income Statement.csv')
    data= data.iloc[[1],[2,3,4,5,6]]
    df=pd.DataFrame(data)
    df.to_csv('In.csv')
    Tcsv1('In.csv','out.csv')

def highlight_cols(s):
    return 'background-color: % s' % 'yellow'

def app():
    col1,col2 = st.columns([3,1])
    col11, col12,col13 = st.columns(3)
    Data=LoadData()
    df = LoadData2()
    df2 = LoadData3()
    #stock_plot.show()
    with st.container():
        with col1:
            st.header('Stock Open Prices')
            stock_plot = px.line(x='Date', y='Open', data_frame=Data,width=1200)
            fig = stock_plot.update_traces(line_color='lightgreen')
            st.plotly_chart(fig)
        with col2:
            st.header('Scoring Criteria')
            st.write(df.style.highlight_max(color='lightgreen').applymap(highlight_cols, subset = df.iloc[2,1]))
    with st.container():
        with col11 :
            Transpose()
            data = pd.read_csv('out.csv')
            data.columns = ["Year", "Income"]
            df = pd.DataFrame(data)
            df.iat[0, df.columns.get_loc('Year')] = '12/31/2022'
            fig = px.bar(df, x='Year', y='Income',width=500,title="Total Income",)
            st.title('Total Assets')
            fig =fig.update_traces(marker_color='lightgreen')
            st.plotly_chart(fig)
        with col12:
            Transpose()
            data = pd.read_csv('out.csv')
            data.columns = ["Year", "Income"]
            df = pd.DataFrame(data)
            df.iat[0, df.columns.get_loc('Year')] = '12/31/2022'
            fig = px.bar(df, x='Year', y='Income', width=500, title="Total Debt", )
            st.title('Total Debt')
            fig = fig.update_traces(marker_color='Red')
            st.plotly_chart(fig)
        with col13:
            Transpose()
            data = pd.read_csv('out.csv')
            data.columns = ["Year", "Income"]
            df = pd.DataFrame(data)
            df.iat[0, df.columns.get_loc('Year')] = '12/31/2022'
            fig = px.bar(df, x='Year', y='Income', width=500, title="Total Equity", )
            st.title('Total Equity')
            fig = fig.update_traces(marker_color='lightgreen')
            st.plotly_chart(fig)
    with st.container():
        with col11:
            st.title('Revenue')
            stock_plot = px.line(x='Date', y='Open', data_frame=Data,width=500)
            fig = stock_plot.update_traces(line_color='lightgreen')
            st.plotly_chart(fig)
        with col12:
            st.title('Total Expanses')
            stock_plot = px.line(x='Date', y='Open', data_frame=Data,width=500)
            fig = stock_plot.update_traces(line_color='Red')
            st.plotly_chart(fig)
        with col13:
            st.title('Net Income')
            stock_plot = px.line(x='Date', y='Open', data_frame=Data,width=500)
            fig = stock_plot.update_traces(line_color='lightgreen')
            st.plotly_chart(fig)
