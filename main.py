import csv
import io
import random
from urllib.request import urlopen, Request

import matplotlib.pyplot as plt
import pandas as pd
import requests
import yahoo_fin.stock_info as yf
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

##############################################################"
# Scrape S&P 500 companies from Wikipedia#
# Create CSV file with scraped company info


################# Acquires Wikipedia page content for S&P500 comp
wicki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
req = Request(url=wicki_url, headers={'user-agent': 'my-app'})
response_1 = urlopen(req)
company_page_content = BeautifulSoup(response_1, 'html.parser')
#####################
# Stores the table with company info into the company table variable
table_id = "constituents"
company_table = company_page_content.find('table', attrs={'id': table_id})
################# Creates a dataframe with company info and writes to CSV
df = pd.read_html(str(company_table))
df[0].to_csv('00. S&P500 company Information.csv')

#############################################
#### Create a data frame from the CSV and randomly select 1 Ticker (Company Acronymes)
csv_df = pd.read_csv('00. S&P500 company Information.csv')  # Reads the generated CSV
company_list = csv_df['Symbol'].to_list()  # Creates a list of companies
random_company = random.sample(company_list, 1)  # Randomly select 1 company from company_list
stock = ''.join(random_company)  # Establishes the randomly selected stock var as a String


################ Scrape the Yahoo Finance Site for financial statements for the selected Ticker ########

def conv_to_num(
        column):  ### function that makes all values numerical - will be needed in the below financial statement scraping
    first_col = [val.replace(',', '') for val in column]
    second_col = [val.replace('-', '') for val in first_col]
    final_col = pd.to_numeric(second_col)
    return final_col


stock = ''.join(random_company)  ####Esatablish the randomly selected stock var as a String
url_inc_statement = 'https://finance.yahoo.com/quote/{}/financials?p={}'  # Establishes URLs for Financial Statements
url_bs_statement = 'https://finance.yahoo.com/quote/{}/balance-sheet?p={}'
url_cf_statement = 'https://finance.yahoo.com/quote/{}/cash-flow?p={}'
##Place these URLs in a list
url_list = [url_inc_statement, url_bs_statement, url_cf_statement]

statement_count = 0
for statement in url_list:
    req = Request(statement.format(stock, stock),
                  headers={'user-agent': 'my-app'})  # Acquires company finacial statement page content
    response_2 = urlopen(req)
    fin_content = BeautifulSoup(response_2, 'html.parser')
    fin_data = fin_content.find_all('div', class_='D(tbr)')
    headres = []
    temp_list = []
    label_list = []
    final = []
    index = 0
    for item in fin_data[0].find_all('div', class_='D(ib)'):  # Creates Headers for statement
        headres.append(item.text)

    while index <= len(fin_data) - 1:  # Statement Contents
        temp = fin_data[index].find_all('div', class_='D(tbc)')
        for line in temp:
            temp_list.append(line.text)
        final.append(temp_list)
        temp_list = []
        index += 1
    df = pd.DataFrame(final[1:])  # places statement contents into a dataframe
    df.columns = headres
    for column in headres[1:]:  # makes all values numerical
        df[column] = conv_to_num(df[column])

    final_df = df.fillna('0')

    statement_count += 1
    if statement_count == 1:  # Used as a naming input for the CSV export below
        final_df.to_csv(f'01. {stock} Income Statement.csv')  # Writes to CSV for each financial statement
    elif statement_count == 2:
        final_df.to_csv(f'02. {stock} Balance Sheet.csv')
    else:
        final_df.to_csv(f'03. {stock} Cash Flow Statement.csv')

####### Scrape the Yahoo Finance Site for stock price history for the selected Ticker

stock_url = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval={}&events={}'  # Acquires stock price history for the selected Ticker

p1='1620055948'
p2='1651591948'
interv='1d'
events='history'
prarms = {
    'range': '5y',
    'interval': '1d',  # Parameters for 5 years of stock history
    'events': 'history'
}
response_3 = requests.get(stock_url.format(stock,p1,p2,interv,events),headers={'user-agent': 'my-app'})  # Acquires the data from the page given above
price_file = io.StringIO(response_3.text)
reader = csv.reader(price_file)
data = list(reader)  # Puts the stock price data into a list
price_df = pd.DataFrame(data)  # creates a stock price data frame and write to CSV
price_df.to_csv(f'04. {stock} Stock Price - 5 Year Historical.csv')

###Scrape the Yahoo Finance site for key statistics for the selected Ticker
base_url = "https://finance.yahoo.com/"
path = "quote/{0}/key-statistics?p={0}".format(stock)
url = base_url + path
hedrs = {"authority": "finance.yahoo.com",
         "method": "GET",
         "path": path,
         "scheme": "https",
         "accept": "text/html,application/xml;q=0.9",
         "accept-encoding": "gzip, deflate, br",
         "accept-language": "en-US,en;q=0.9",
         "referer": base_url,
         "sec-fetch-mode": "navigate",
         "sec-fetch-site": "same-origin",
         "sec-fetch-user": "?1",
         "upgrade-insecure-requests": "1",
         "user-agent": "Mozilla/5.0 (Windows NT 10.0;)"}
page = requests.get(url, headers=hedrs)
soup = BeautifulSoup(page.content, 'lxml')
tables = soup.find_all('table')
iterator = range(0, len(tables))
function = lambda x: pd.read_html(str(tables[x]))
table_list = list(map(function, iterator))
stats_df = pd.DataFrame(table_list)  # Create data frame with statistics
stats_df.to_csv(f'05.{stock} Statistics.csv')  # write the dataframe to CSV

############### Create a multi-layred stock screen to dertemine company's financial strength


##Importing Yahoo Finance module for the finacial items that were not able ti be scraped
yf_bs = []
yf_is = []
yf_cf = []
years = []

yf_bs = yf.get_balance_sheet(stock)
yf_is = yf.get_income_statement(stock)
yf_cf = yf.get_cash_flow(stock)
years = yf_bs.columns

############### Fundemental anlysis using web scraped data
income_statement = pd.read_csv(
    f'01. {stock} Income Statement.csv')  # Reads in the financial statement CSVs that were generated as well as the years
balance_sheet = pd.read_csv(f'02. {stock} Balance Sheet.csv')
cashflow_statement = pd.read_csv(f'03. {stock} Cash Flow Statement.csv')
years = list(income_statement.columns[3:6])
##################
income_statement.drop(income_statement.columns[0], axis=1, inplace=True)  # Remove 1st column from dataframes
balance_sheet.drop(balance_sheet.columns[0], axis=1, inplace=True)
cashflow_statement.drop(cashflow_statement.columns[0], axis=1, inplace=True)

##########" Initialize scoring tracker

profitability_score = 0
leverage_liquidity_score = 0
operating_efficiency_score = 0


###############"
def profitability():
    global profitability_score
    roa_cy = float(income_statement.iloc[4, 2]) / float(balance_sheet.iloc[0, 1])
    roa_py = income_statement.iloc[4, 3] / balance_sheet.iloc[0, 2]
    cfo_cy = cashflow_statement.iloc[0, 2]
    cfo_py = cashflow_statement.iloc[0, 3]

    if roa_cy > 0:  # return on assets logic
        profitability_score += 1
    if roa_cy - roa_py > 0:
        profitability_score += 1
    else:
        profitability_score += 0
    if cfo_cy > 0:  ## cash flow form operations logic
        profitability_score += 1
    if cfo_cy - cfo_py > 0:
        profitability_score += 1
    else:
        profitability_score += 0

    return profitability_score


def leverage():
    global leverage_liquidity_score
    lever_cy = balance_sheet.iloc[8, 2] / balance_sheet.iloc[0, 1]
    lever_py = balance_sheet.iloc[8, 2] / balance_sheet.iloc[0, 2]
    cur_ratio_cy = yf_bs.iloc[15, 0] / yf_bs.iloc[13, 0]
    cur_ratio_py = yf_bs.iloc[15, 1] / yf_bs.iloc[13, 1]
    share_cy = balance_sheet.iloc[10, 1]
    share_py = balance_sheet.iloc[10, 2]

    if lever_cy - lever_py > 0:  # leverage logic
        leverage_liquidity_score += 1
    else:
        leverage_liquidity_score += 0

    if cur_ratio_cy - cur_ratio_py > 0:  # liquidity logic
        leverage_liquidity_score += 1
    else:
        leverage_liquidity_score += 0

    if cur_ratio_cy - share_py < 0:  # shares logic
        leverage_liquidity_score += 1
    else:
        leverage_liquidity_score += 0

    return leverage_liquidity_score


def operating_efficiency():
    global operating_efficiency_score
    gm_cy = yf_is.iloc[6, 0] / yf_is.iloc[15, 0]
    gm_py = yf_is.iloc[6, 1] / yf_is.iloc[15, 1]
    turn_cy = balance_sheet.iloc[0, 2] / ((balance_sheet.iloc[0, 1] + balance_sheet.iloc[0, 2]) / 2)
    turn_py = balance_sheet.iloc[0, 3] / ((balance_sheet.iloc[0, 2] + balance_sheet.iloc[0, 3]) / 2)

    if gm_cy - gm_py > 0:  # gm locgic
        operating_efficiency_score += 1
    else:
        operating_efficiency_score += 0
    if turn_cy - turn_py > 0:  # assets turnover ratio logic
        operating_efficiency_score += 1
    else:
        operating_efficiency_score += 0

    return operating_efficiency_score


#########

###Export Financial Strength Scoring CSV
p_score = profitability()
lev_score = leverage()
oper_score = operating_efficiency()

fin_strength_scores = {'Profitability Score': p_score,
                       'Leverage and Liquidity Score': lev_score,
                       'Operating Efficiency Score': oper_score,
                       'Total Score': p_score + lev_score + oper_score}
fin_strength_df = pd.DataFrame(list(fin_strength_scores.items()), columns=['Scoring Criteria', 'Score'])
fin_strength_df.to_csv(f'06.{stock} Piotroski Score Results.csv')

#############################################
###Scrape Finviz news article headings #########"
finviz_url = f'https://finviz.com/quote.ashx?t={stock}'
req = Request(url=finviz_url, headers={'user-agent': 'my-analysis'})
response = urlopen(req)
html = BeautifulSoup(response, 'html')
news_tables = {}
news_table = html.find(id='news-table')
news_tables[stock] = news_table
stock_data = news_tables[stock]
stock_rows = stock_data.findAll('tr')

parsed_data = []
for stock, news_table in news_tables.items():
    for row in news_table.findAll('tr'):
        title = row.a.text
        date_data = row.td.text.split(' ')

        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([stock, date, time, title])

#################################
# Perform Sentiment analysis on news article heaadings using the nltk.sentement.vader.package
news_df = pd.DataFrame(parsed_data, columns=['stock', 'date', 'time', 'heading'])
vader = SentimentIntensityAnalyzer()
lambda_func = lambda title: vader.polarity_scores(title)['compound']
news_df['compound score'] = news_df['heading'].apply(lambda_func)
news_df['date'] = pd.to_datetime(news_df.date).dt.date
news_df.to_csv(f'07.{stock} Sentiment Analysis.csv')

############################
# Visualization of Sentiment Analysis
mean_df = news_df.groupby(['date']).mean()
plt.plot(mean_df, color='blue')
plt.title(f'{stock} Mean Compound Score Over Time')
plt.axhline(0, color='red')
plt.savefig(f'08.{stock} Compound Score.png', format='png', dpi=200, bbox_inches='tight', orientation='landscape')
