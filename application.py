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
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html


# In[ ]:


# builds app layout

external_stylesheets=['https://raw.githubusercontent.com/pmshea/oil-gas-project/master/assets/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

application = app.server

app.layout = html.Div([
    
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([html.H6('S&P', style={'margin-bottom':'0px'})], style={'margin-bottom':'0px'}),
                        html.Div(
                            id='sp_output', 
                            style={'text-align':'center', 
                                   'font-size':'12px', 
                                   'font-family':'helvetica', 
                                   'margin-top':'0px'}
                        ), 
                        html.Div(
                            id='sp_change', 
                            style={'text-align':'center', 
                                   'font-size':'10px', 
                                   'font-family':'helvetica'}
                        )
                    ])
                ], className='column', style={'textAlign':'center'}),
                
                html.Div([
                    html.Div([
                        html.Div([html.H6('DOW', style={'margin-bottom':'0px'})], style={'margin-bottom':'0px'}),
                        html.Div(id='dow_jones_output', 
                            style={'text-align':'center', 
                                   'font-size':'12px', 
                                   'font-family':'helvetica'}
                        ), 
                    
                        html.Div(
                            id='dow_jones_change', 
                            style={'text-align':'center', 
                                   'font-size':'10px', 
                                   'font-family':'helvetica'}
                        )
                    ])
                ], className='column', style={'textAlign':'center', 'margin-left':'30px'}),
                
                html.Div([
                    html.Div([
                        html.Div([html.H6('NASDAQ', style={'margin-bottom':'0px'})], style={'margin-bottom':'0px'}),
                        html.Div(id='nasdaq_output', 
                            style={'text-align':'center',
                                   'font-size':'12px', 
                                   'font-family':'helvetica'}
                        ), 
                        
                        html.Div(
                            id='nasdaq_change', 
                            style={'text-align':'center', 
                                   'font-size':'10px', 
                                   'font-family':'helvetica'}
                        )                        
                    ])
                ], className='column', style={'textAlign':'center', 'margin-left':'30px'})
            ], className='row'
            ), 
        ], className='column', style={'textAlign': 'left', 'margin-left':'110px'}
        ),
        
        html.Div([
            html.H3(
                "OIL & GAS TODAY",
                className="app__header__title", 
                style={"margin-bottom": "0px",
                       "textAlign": "center"}
            ),
            html.H5("SELECT MARKET DATA", style={"margin-top": "0px", "textAlign": "center"})
        ], className='column', style={'textAlign': 'center', 'margin-left':'215px'}
        ), 
        
        html.Div([
            html.H3('PARKER M. SHEA', style={'textAlign': 'center'})
        ], className='column', style={'textAlign': 'right', 'margin-left':'350px', 'margin-top':'15px'}
        )
    ],
    className="row",
    id="title",
    style={'margin-bottom':'10px'}
    ),
    
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H5('CURRENT PRICE OF', style={'align':'left', 'margin-left':'50px', 'margin-top':'6px'})
                    ], className='column'),
                    html.Div([
                        dcc.Dropdown(
                            id='my_dropdown',
                            options=[
                                {'label': 'GAZPROM', 'value': 'OGZPY'},
                                {'label': 'EXXON MOBIL', 'value': 'XOM'},
                                {'label': 'PETROCHINA COMPANY', 'value': 'PTR'},
                                {'label': 'ROYAL DUTCH SHELL', 'value': 'RDS-A'},
                                {'label': 'BP', 'value': 'BP'},
                                {'label': 'CHEVRON', 'value': 'CVX'},
                                {'label': 'TOTAL', 'value': 'TOT'},
                                {'label': 'EQUINOR', 'value': 'EQNR'},
                                {'label': 'COCONOPHILLIPS', 'value': 'COP'},
                                {'label': 'ENI', 'value': 'E'}
                            ],
                            value='OGZPY',
                            multi=False,
                            clearable=False,
                            style={'padding-top':'0px', 
                                   'margin-top':'0px', 
                                   'width':'200px', 
                                   'margin-left':'6px', 
                                   'align':'right'} 
                        )                        
                    ], className='column')
                ], style={'margin-bottom':'5px', 
                          'margin-left':'25px', 
                          'margin-right':'0px',
                          'backgroundColor':'black'}, className='row'
                ),
            
                html.Div(id='price_output', 
                         style={'text-align':'center', 
                                'color':'rgb(99, 110, 250)',
                                'font-size':'80px', 
                                'font-family':'helvetica'}
                ), 
                html.Div([
                    html.Div([html.H3('ETFS & COMMODITY PRICES', style={'text-align':'center'})], 
                             style={'backgroundColor':'black', 'margin-left':'25px', 'margin-bottom':'25px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.H3('CRUDE OIL', style={'textAlign':'center', 'backgroundColor':'black', 'margin-bottom':'0px'})
                                ], style={'margin-bottom':'0px', 'textAlign':'center'}
                                ),
                                html.Div(
                                    id='crude_oil_output', 
                                    style={'text-align':'center', 
                                           'font-size':'45px', 
                                           'font-family':'helvetica', 
                                           'margin-bottom':'0px',
                                           'margin-top':'0px'}
                                ),
                                html.Div(
                                    id='crude_oil_change',
                                    style={'text-align':'center', 
                                           'font-size':'30px', 
                                           'font-family':'helvetica', 
                                           'margin-bottom':'0px',
                                           'margin-top':'0px'}
                                )
                            ], style={'textAlign':'center'}
                            ),

                            html.Div([
                                html.Div([
                                    html.H3('NAT. GAS', style={'textAlign':'center', 'backgroundColor':'black', 'margin-bottom':'0px'})
                                ], style={'margin-bottom':'0px'}
                                ),
                                html.Div(
                                    id='nat_gas_output', 
                                    style={'text-align':'center', 
                                           'font-size':'45px', 
                                           'font-family':'helvetica', 
                                           'margin-bottom':'0px',
                                           'margin-top':'0px'}
                                ),
                                html.Div(
                                    id='nat_gas_change',
                                    style={'text-align':'center', 
                                           'font-size':'30px', 
                                           'font-family':'helvetica', 
                                           'margin-bottom':'0px',
                                           'margin-top':'0px'}                               
                                )
                            ], style={'textAlign':'center'}
                            ), 

                            html.Div([
                                html.Div([
                                    html.H3('DJUSEN', style={'textAlign':'center', 'backgroundColor':'black', 'margin-bottom':'0px'})
                                ], style={'margin-bottom':'0px'}
                                ),
                                html.Div(
                                    id='djusen_output', 
                                    style={'text-align':'center', 
                                           'font-size':'45px', 
                                           'font-family':'helvetica', 
                                           'margin-bottom':'0px',
                                           'margin-top':'0px'}
                                ),
                                html.Div(
                                    id='djusen_change',
                                    style={'text-align':'center', 
                                           'font-size':'30px', 
                                           'font-family':'helvetica', 
                                           'margin-bottom':'0px',
                                           'margin-top':'0px'}
                                )
                            ], style={'textAlign':'center'}
                            )
                        ], className='column', style={'margin-left':'55px'}
                        ),

                        html.Div([
                            html.Div([
                                html.Div([
                                    html.H3('XOP', style={'textAlign':'center', 'backgroundColor':'black', 'margin-bottom':'0px'})
                                ], style={'margin-bottom':'0px'}
                                ),
                                html.Div(
                                    id='xop_output', 
                                    style={'text-align':'center', 
                                           'font-size':'45px', 
                                           'font-family':'helvetica', 
                                           'margin-bottom':'0px',
                                           'margin-top':'0px'}
                                ),
                                html.Div(
                                    id='xop_change',
                                    style={'text-align':'center', 
                                           'font-size':'30px', 
                                           'font-family':'helvetica', 
                                           'margin-bottom':'0px',
                                           'margin-top':'0px'}
                                )                            
                            ], style={'textAlign':'center'}
                            ),

                            html.Div([
                                html.Div([
                                    html.H3('IEO', style={'textAlign':'center', 'backgroundColor':'black', 'margin-bottom':'0px'})
                                ], style={'margin-bottom':'0px'}
                                ),
                                html.Div(
                                    id='ieo_output', 
                                    style={'text-align':'center', 
                                           'font-size':'45px', 
                                           'font-family':'helvetica', 
                                           'margin-bottom':'0px',
                                           'margin-top':'0px'}
                                ),
                                html.Div(
                                    id='ieo_change',
                                    style={'text-align':'center', 
                                           'font-size':'30px', 
                                           'font-family':'helvetica', 
                                           'margin-bottom':'0px',
                                           'margin-top':'0px'}
                                )                            
                            ], style={'textAlign':'center'}
                            ),

                            html.Div([
                                html.Div([
                                    html.H3('PXE', style={'textAlign':'center', 'backgroundColor':'black', 'margin-bottom':'0px'})
                                ], style={'margin-bottom':'0px'}
                                ),
                                html.Div(
                                    id='pxe_output', 
                                    style={'text-align':'center', 
                                           'font-size':'45px', 
                                           'font-family':'helvetica', 
                                           'margin-bottom':'0px',
                                           'margin-top':'0px'}
                                ),
                                html.Div(
                                    id='pxe_change',
                                    style={'text-align':'center', 
                                           'font-size':'30px', 
                                           'font-family':'helvetica', 
                                           'margin-bottom':'0px',
                                           'margin-top':'0px'}
                                )                            
                            ], style={'textAlign':'center'}
                            )
                        ], className='column', style={'margin-left':'50px'}
                        )
                    ], className='row'
                    )
                ])
            ], style={'margin-bottom':'30px'}
            )
        ],
        className='column', style={'width':'40%'}
        ), 
        
        html.Div([
            html.Div([dcc.Graph(id='last_thirty_graph', style={'height': '330px'})]),
            
            html.Div([dcc.Graph(id='historical_graph', style={'height':'330px'})])
        ],
        className='column', style={'width':'875px', 'margin-left':'25px', 'margin-right':'0px'}
        )
    ], className='row'
    )
])

@app.callback(
    [dash.dependencies.Output('last_thirty_graph', 'figure'),
     dash.dependencies.Output('price_output', 'children'),
     dash.dependencies.Output('historical_graph', 'figure'),
     dash.dependencies.Output('sp_output', 'children'),
     dash.dependencies.Output('sp_change', 'children'),
     dash.dependencies.Output('dow_jones_output', 'children'),
     dash.dependencies.Output('dow_jones_change', 'children'),
     dash.dependencies.Output('nasdaq_output', 'children'),
     dash.dependencies.Output('nasdaq_change', 'children'),
     dash.dependencies.Output('crude_oil_output', 'children'),
     dash.dependencies.Output('crude_oil_change', 'children'),
     dash.dependencies.Output('nat_gas_output', 'children'),
     dash.dependencies.Output('nat_gas_change', 'children'),
     dash.dependencies.Output('djusen_output', 'children'),
     dash.dependencies.Output('djusen_change', 'children'),
     dash.dependencies.Output('xop_output', 'children'),
     dash.dependencies.Output('xop_change', 'children'),
     dash.dependencies.Output('ieo_output', 'children'),
     dash.dependencies.Output('ieo_change', 'children'),
     dash.dependencies.Output('pxe_output', 'children'),
     dash.dependencies.Output('pxe_change', 'children'),
     dash.dependencies.Output('sp_change', 'style'),
     dash.dependencies.Output('dow_jones_change', 'style'),
     dash.dependencies.Output('nasdaq_change', 'style'),
     dash.dependencies.Output('crude_oil_change', 'style'),
     dash.dependencies.Output('nat_gas_change', 'style'),
     dash.dependencies.Output('djusen_change', 'style'),
     dash.dependencies.Output('xop_change', 'style'),
     dash.dependencies.Output('ieo_change', 'style'),
     dash.dependencies.Output('pxe_change', 'style')],
    [dash.dependencies.Input('my_dropdown', 'value')])

def update_output(selected_firm):

# creates last thirty days price chart
    
    df = pd.read_csv('https://raw.githubusercontent.com/pmshea/oil-gas-project/master/' + 'Short_' + selected_firm + '.csv')
    thirty_days_chart = px.line(
                     data_frame = df, 
                     x='Date',
                     y='Close',
                     title=selected_firm +': LAST THIRTY DAYS',
                     template='plotly_dark',
                     labels={'Date':'', 'Close':''}
    )
    
    thirty_days_chart.update_layout(title={'x':0.5, 'xanchor': 'center'})
    
# scrapes selected_firm price

    link = ('https://finance.yahoo.com/quote/' + selected_firm + '?p=OGZPY&.tsrc=fin-srch')
    r=requests.get(link)
    soup=bs4.BeautifulSoup(r.text, 'html')
    price = soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    
# creates historical price chart

    df2 = pd.read_csv('https://github.com/pmshea/oil-gas-project/blob/master/' + selected_firm + '.csv')
    historical_chart = px.area(
                     data_frame = df2,
                     x='Date',
                     y='Close',
                     title=selected_firm + ': HISTORICAL',
                     template='plotly_dark',
                     labels={'Date':'', 'Close':''}
    )
    
    historical_chart.update_layout(title={'x':0.5, 'xanchor': 'center'})
    
# scrapes s&p price

    sp_link = ('https://finance.yahoo.com/quote/%5EGSPC/')
    sp_r=requests.get(sp_link)
    sp_soup=bs4.BeautifulSoup(sp_r.text, 'html')
    sp_price = sp_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    sp_change = sp_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find_all('span')[1].text
    if '-' in sp_change: 
        sp_color = {'color':'red'}
    else:
        sp_color = {'color':'green'}

# scrapes dow jones price

    dow_link = ('https://finance.yahoo.com/quote/%5EDJI?p=%5EDJI')
    dow_r=requests.get(dow_link)
    dow_soup=bs4.BeautifulSoup(dow_r.text, 'html')
    dow_price = dow_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    dow_change = dow_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find_all('span')[1].text

# scrapes nasdaq price

    nasdaq_link = ('https://finance.yahoo.com/quote/%5EIXIC/')
    nasdaq_r=requests.get(nasdaq_link)
    nasdaq_soup=bs4.BeautifulSoup(nasdaq_r.text, 'html')
    nasdaq_price = nasdaq_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    nasdaq_change = nasdaq_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find_all('span')[1].text

# scrapes crude oil price

    crude_link = ('https://finance.yahoo.com/quote/CL=F/')
    crude_r=requests.get(crude_link)
    crude_soup=bs4.BeautifulSoup(crude_r.text, 'html')
    crude_price = crude_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    crude_change = crude_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find_all('span')[1].text

# scrapes natural gas price

    gas_link = ('https://finance.yahoo.com/quote/NG%3DF/')
    gas_r=requests.get(gas_link)
    gas_soup=bs4.BeautifulSoup(gas_r.text, 'html')
    gas_price = gas_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    gas_change = gas_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find_all('span')[1].text

# scrapes djusen index price

    djusen_link = ('https://finance.yahoo.com/quote/%5EDJUSEN?ltr=1')
    djusen_r=requests.get(djusen_link)
    djusen_soup=bs4.BeautifulSoup(djusen_r.text, 'html')
    djusen_price = djusen_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    djusen_change = djusen_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find_all('span')[1].text

# scrapes XOP price

    xop_link = ('https://finance.yahoo.com/quote/xop/')
    xop_r=requests.get(xop_link)
    xop_soup=bs4.BeautifulSoup(xop_r.text, 'html')
    xop_price = xop_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    xop_change = xop_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find_all('span')[1].text

# scrapes IEO price

    ieo_link = ('https://finance.yahoo.com/quote/IEO/')
    ieo_r=requests.get(ieo_link)
    ieo_soup=bs4.BeautifulSoup(ieo_r.text, 'html')
    ieo_price = ieo_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    ieo_change = ieo_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find_all('span')[1].text

# scrapes PXE price
        
    pxe_link = ('https://finance.yahoo.com/quote/pxe/')
    pxe_r=requests.get(pxe_link)
    pxe_soup=bs4.BeautifulSoup(pxe_r.text, 'html')
    pxe_price = pxe_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    pxe_change = pxe_soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find_all('span')[1].text
    
    if '-' in sp_change: 
        sp_color = {'color':'red'}
    else:
        sp_color = {'color':'green'}
        
    if '-' in dow_change: 
        dow_color = {'color':'red'}
    else:
        dow_color = {'color':'green'}

    if '-' in nasdaq_change: 
        nasdaq_color = {'color':'red'}
    else:
        nasdaq_color = {'color':'green'}
        
    if '-' in crude_change: 
        crude_color = {'color':'red', 'font-size':'30px'}
    else:
        crude_color = {'color':'green', 'font-size':'30px'}
        
    if '-' in gas_change: 
        gas_color = {'color':'red', 'font-size':'30px'}
    else:
        gas_color = {'color':'green', 'font-size':'30px'}
        
    if '-' in djusen_change: 
        djusen_color = {'color':'red', 'font-size':'30px'}
    else:
        djusen_color = {'color':'green', 'font-size':'30px'}
    
    if '-' in xop_change: 
        xop_color = {'color':'red', 'font-size':'30px'}
    else:
        xop_color = {'color':'green', 'font-size':'30px'}

    if '-' in ieo_change: 
        ieo_color = {'color':'red', 'font-size':'30px'}
    else:
        ieo_color = {'color':'green', 'font-size':'30px'}
    
    if '-' in pxe_change: 
        pxe_color = {'color':'red', 'font-size':'30px'}
    else:
        pxe_color = {'color':'green', 'font-size':'30px'}
    
    return thirty_days_chart, ('$' + price + ' USD'), historical_chart, ('$' + sp_price + ' USD'), sp_change,          ('$' + dow_price + ' USD'), dow_change, ('$' + nasdaq_price + ' USD'), nasdaq_change,          ('$' + crude_price + ' USD'), crude_change, ('$' + gas_price + ' USD'), gas_change,          ('$' + djusen_price + ' USD'), djusen_change, ('$' + xop_price + ' USD'), xop_change,          ('$' + ieo_price + ' USD'), ieo_change, ('$' + pxe_price + ' USD'), pxe_change, sp_color, dow_color,          nasdaq_color, crude_color, gas_color, djusen_color, xop_color, ieo_color, pxe_color

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)

