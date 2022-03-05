import csv
import io
import random
import  urllib
from io import StringIO
from urllib.parse import urlencode
from urllib.request import urlopen, Request

import params as params
import requests as requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
from urllib3.packages.six import StringIO

wicki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
req = Request(url=wicki_url, headers={'user-agent': 'my-app'})
response_1 = urlopen(req)
company_page_content = BeautifulSoup(response_1, 'html.parser')

table_id = "constituents"
company_table = company_page_content.find('table', attrs={'id': table_id})
df = pd.read_html(str(company_table))
df[0].to_csv('00. S&P500 company Information.csv')
csv_df = pd.read_csv('00. S&P500 company Information.csv')
company_list = csv_df['Symbol'].to_list()
random_company = random.sample(company_list, 1)
stock = ''.join(random_company)


def conv_to_num(column):
    first_col = [val.replace(',', '') for val in column]
    second_col = [val.replace('-', '') for val in first_col]
    final_col = pd.to_numeric(second_col)
    return final_col


stock = ''.join(random_company)
url_inc_statement = 'https://finance.yahoo.com/quote/{}/financials?p={}'
url_bs_statement = 'https://finance.yahoo.com/quote/{}/balance-sheet?p={}'
url_cf_statement='https://finance.yahoo.com/quote/{}/cash-flow?p={}'
url_list = [url_inc_statement, url_bs_statement, url_cf_statement]
statement_count = 0
for statement in url_list:
    req = Request(statement.format(stock,stock), headers={'user-agent': 'my-app'})
    response_2 = urlopen(req)
    fin_content = BeautifulSoup(response_2,'html.parser')
    fin_data = fin_content.find_all('div',class_='D(tbr)')
    headres = []
    temp_list = []
    label_list = []
    final = []
    index = 0
    for item in fin_data[0].find_all('div',class_='D(ib)'):
        headres.append(item.text)

    while index <= len(fin_data)-1 :
        temp = fin_data[index].find_all('div',class_='D(tbc)')
        for line in temp:
            temp_list.append(line.text)
        final.append(temp_list)
        temp_list=[]
        index += 1
    df = pd.DataFrame(final[1:])
    df.columns = headres
    for column in headres[1:]:
        df[column] = conv_to_num(df[column])

    final_df = df.fillna('0')

    statement_count += 1
    if statement_count == 1:
        final_df.to_csv(f'01. {stock} Income Statement.csv')
    elif statement_count == 2:
        final_df.to_csv(f'02. {stock} Balance Sheet.csv')
    else:
        final_df.to_csv(f'03. {stock} Cash Flow Statement.csv')

stock_url = 'https://query1.finance.yahoo.com/v7/finance/download/{}'

prarms = {
    'range': '5y',
    'interval': '1d',
    'events': 'history'
}
req=Request(stock_url.format(stock), headers={'user-agent': 'my-app'})
response_3 = urlopen(req)
price_file = io.StringIO(response_3.read().decode('utf-8'))
reader = csv.reader(price_file)
data = list(reader)
price_df = pd.DataFrame(data)
price_df.to_csv(f'04. {stock} Stock Price - 5 Year Historical.csv')
url = 'https://fincance.yahoo.com/quote/{}/key-statistics?p={}'
#r = requests.get(url.format(stock,stock))
#r=Request(url.format(stock,stock), headers={'user-agent': 'my-app'})
#r = urlopen(req)
stats = pd.read_html(url.format(stock,stock))
print(stats)
#key_stats = stats[0]
#stats_df = pd.DataFrame(key_stats)

#print(stats_df)

