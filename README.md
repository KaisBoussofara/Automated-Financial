# Deepfake Image Authenticity & Financial Sentiment Project

## Overview

This project provides a web application that can for a randomly selected S&P 500 ticker, collect financial information and analyze the sentiment of related news. The system is designed for educational and research purposes to illustrate how machine learning, web scraping, and natural-language sentiment tools can be integrated in a single workflow.

Main capabilities:

- Scrape the list of S&P 500 companies from Wikipedia  
- Download Yahoo Finance statements for one selected ticker  
- Compute ratio-based financial strength scores  
- Scrape Finviz news headings and evaluate their sentiment with VADER  
- Produce CSV and PNG artifacts for reporting

---

## Components


### 2) Company Information Scraper

- The program downloads the Wikipedia page:  
  `List_of_S&P_500_companies`
- The table with id **“constituents”** is converted to a DataFrame  
- The file is stored as:  
  `00. S&P500 company Information.csv`

---

### 3) Financial Statements Collector

For the selected ticker symbol, the script retrieves:

- Income Statement  
- Balance Sheet  
- Cash Flow Statement  
- 5-Year price history  
- Key statistics

All numeric columns are converted using the helper function `conv_to_num()` to ensure that ratios can be calculated.

Generated files:

- `01. <stock> Income Statement.csv`  
- `02. <stock> Balance Sheet.csv`  
- `03. <stock> Cash Flow Statement.csv`  
- `04. <stock> Stock Price – 5 Year Historical.csv`  
- `05. <stock> Statistics.csv`

---

### 4) Financial Strength Scoring

Three functions implement the screen logic:

- `profitability()` – based on return on assets and operating cash flow  
- `leverage()` – based on leverage, liquidity, and share evolution  
- `operating_efficiency()` – based on gross margin and asset turnover

Results are summarized as:

- `06. <stock> Piotroski Score Results.csv`

---

### 5) Sentiment Analysis

- Finviz article headings are scraped  
- Sentiment is evaluated using:  
  `vaderSentiment.SentimentIntensityAnalyzer`

Output:

- `07. <stock> Sentiment Analysis.csv`  
- `08. <stock> Compound Score.png`

---

## Dependencies

- Python 3.10+  
- pandas  
- beautifulsoup4  
- yahoo_fin  
- vaderSentiment  
- matplotlib  
- scipy  
- joblib  
- requests

Install all:

```bash
pip install -r requirements.txt
