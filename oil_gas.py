#!/usr/bin/env python
# coding: utf-8

# In[1]:


import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import re
import time

import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html


# In[ ]:


#builds scraping function and live dataframes

def date_time_extractor(x):
    match = []
    if re.search(r'\d{2}:\d{2}', x) is not None:
        match = re.search(r'\d{2}:\d{2}', x)
    else: 
        match = re.search(r'\d{1}:\d{2}', x)
    time = datetime.datetime.strptime(match.group(), '%H:%M').time()
    date_time = datetime.datetime.combine(datetime.datetime.now().date(), time)
    return date_time

companies = ['OGZPY', 'XOM', 'PTR', 'RDS-A', 'BP', 'CVX', 'TOT', 'EQNR', 'COP', 'E']

def parsePrice():
    price_time_series = pd.DataFrame(columns = ['Time', 'OGZPY', 'XOM', 'PTR', 'RDS-A', 'BP', 'CVX', 'TOT', 'EQNR', 'COP', 'E'])
    for company in companies: 
        link = ('https://finance.yahoo.com/quote/' + company + '?p=OGZPY&.tsrc=fin-srch')
        r=requests.get(link)
        soup=bs4.BeautifulSoup(r.text, 'html')
        price = soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
        time_raw = soup.find_all('div', {'class': 'C($tertiaryColor) D(b) Fz(12px) Fw(n) Mstart(0)--mobpsm Mt(6px)--mobpsm'})[0].find('span').text
        time = date_time_extractor(time_raw)
        company_entry = pd.DataFrame([[time, price]], columns = ['Time', company])
        price_time_series = price_time_series.append(company_entry)
    return price_time_series

thirty_days_of_prices = pd.DataFrame(columns = ['Time', 'OGZPY', 'XOM', 'PTR', 'RDS-A', 'BP', 'CVX', 'TOT', 'EQNR', 'COP', 'E'])

thirty_days_of_prices = thirty_days_of_prices.append(parsePrice())
thirty_days_of_prices.to_csv('price_data.csv', mode='a', header=False)

gazprom_data = thirty_days_of_prices[['Time', 'OGZPY']].dropna()
gazprom_data.to_csv('gazprom_data.csv', mode='a', header=False)

exxon_data = thirty_days_of_prices[['Time', 'XOM']].dropna()
exxon_data.to_csv('exxon_data.csv', mode='a', header=False)

china_petrol_data = thirty_days_of_prices[['Time', 'PTR']].dropna()
china_petrol_data.to_csv('china_petrol_data.csv', mode='a', header=False)

royal_dutch_shell_data = thirty_days_of_prices[['Time', 'RDS-A']].dropna()
royal_dutch_shell_data.to_csv('royal_dutch_shell_data.csv', mode='a', header=False)

BP_data = thirty_days_of_prices[['Time', 'BP']].dropna()
BP_data.to_csv('BP_data.csv', mode='a', header=False)

chevron_data = thirty_days_of_prices[['Time', 'CVX']].dropna()
chevron_data.to_csv('chevron_data.csv', mode='a', header=False)

total_data = thirty_days_of_prices[['Time', 'TOT']].dropna()
total_data.to_csv('total_data.csv', mode='a', header=False)

equinor_data = thirty_days_of_prices[['Time', 'EQNR']].dropna()
equinor_data.to_csv('equinor_data.csv', mode='a', header=False)

cocono_phillips_data = thirty_days_of_prices[['Time', 'COP']].dropna()
cocono_phillips_data.to_csv('cocono_phillips_data.csv', mode='a', header=False)

eni_data = thirty_days_of_prices[['Time', 'E']].dropna()
eni_data.to_csv('eni_data.csv', mode='a', header=False)

# In[ ]:




