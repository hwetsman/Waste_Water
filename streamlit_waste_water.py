#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 12:37:35 2022

@author: howardwetsman
"""


import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


# url = 'https://data.cdc.gov/resource/2ew6-ywp6.json'
# url = 'https://github.com/biobotanalytics/covid19-wastewater-data/blob/6cccf0ee1c4248ece605468096fad2af4bb058b5/wastewater_by_county.csv'


#select state
states = ['Louisiana','Florida','Colorado','Idaho']
state = st.sidebar.selectbox('State of Interest',states)
st.write(state)
url = f'https://data.cdc.gov/resource/2ew6-ywp6.json?wwtp_jurisdiction={state}'
data = requests.get(url)
df = pd.read_json(data.content)
df = df[df.reporting_jurisdiction == state]
counties = list(set(df.county_names.tolist()))
county = st.sidebar.selectbox('County of Interest',counties)

st.write(county)
df = df[df.county_names == county]
plants = list(set(df.wwtp_id.tolist()))

# st.write(plants)
plant = st.sidebar.selectbox('Treatment Plant',plants)
df = df[df.wwtp_id == plant]

st.write(df)



#alternate data source for Orange County
if state == 'Florida' and county == 'Orange':
    url = 'https://raw.githubusercontent.com/biobotanalytics/covid19-wastewater-data/6cccf0ee1c4248ece605468096fad2af4bb058b5/wastewater_by_county.csv'
    df = pd.read_csv(url)
    df.drop('Unnamed: 0',axis=1,inplace=True)
    
    states = ['FL']
    df = df[df.state.isin(states)]
    df = df[df.name == 'Orange County, FL']
    df.sampling_week = pd.to_datetime(df.sampling_week, format='%Y-%m-%d')
    df = df[['sampling_week','effective_concentration_rolling_average']]
    fig = plt.figure(figsize=(12, 5))
    first_day = str(df.sampling_week.min()).split(' ')[0]
    last_day = str(df.sampling_week.max()).split(' ')[0]
    
    fig = plt.figure(figsize=(10,8))
    X = df.sampling_week.tolist()
    Y = df.effective_concentration_rolling_average.tolist()
    plt.plot(X, Y)
    plt.title(f'Orange County Covid Waste Water Testing Data from {first_day} to {last_day}')
    plt.xlabel('Date')
    plt.ylabel('Effective Concentration Rolling Average')
    plt.legend()
    plt.xticks(rotation=70)
    st.pyplot(fig)



df = df[['wwtp_id', 'county_names',  'date_start', 'date_end', 'ptc_15d']]
df = df[~df.ptc_15d.isna()]
df.reset_index(drop=True,inplace=True)
# st.write(type(df.loc[0,'date_start']))
df.sort_values('date_end', inplace=True, axis=0)
df.drop_duplicates(inplace=True)
for i,r in df.iterrows():
    df.loc[i,'date_start'] = pd.to_datetime(df.loc[i,'date_start'], format='%Y-%m-%d')
    df.loc[i,'date_end'] = pd.to_datetime(df.loc[i,'date_end'], format='%Y-%m-%d')
st.write(df)

#get first and last day
starting_dates = df.date_start.tolist()
ending_dates = df.date_end.tolist()
first_day = str(np.array(starting_dates).min()).split(' ')[0]
last_day = str(np.array(ending_dates).max()).split(' ')[0]
st.write(first_day)
st.write(last_day)


#     for plant in plant_dict:
#         df = plant_dict.get(plant)
#         county = df.county_names.tolist()[0]
#         df.reset_index(drop=True, inplace=True)
#         # see if there's enough data
#         
#         start_dates = df.date_start.tolist()
#         first_day = str(np.array(start_dates).min()).split(' ')[0]
#         
#         enough = False
#         for dat in end_dates:
#             if dat in start_dates:
#                 enough = True
    
#         # calculate quantity for first end date forward as start
#         idx_first = df[df.date_start == df.date_end.min()].index[0]
#         for i in range(idx_first, df.index.max()+1, 1):
#             if i == idx_first:
#                 df.loc[i, 'start_quantity'] = 10000
#             else:
#                 base = df.loc[i-1, 'start_quantity']
#                 percent_change = df.loc[i, 'ptc_15d']
#                 delta = df.loc[i, 'ptc_15d']/100*base
#                 new_total = base+delta
#                 df.loc[i, 'start_quantity'] = int(new_total)
    
#         # infer old values
#         to_calculate = df[~df.start_quantity.isna()].date_start.tolist()
#         for dat in to_calculate:
#             calc_idx = df[df.date_end == dat].index[0]
#             base_idx = df[df.date_start == dat].index[0]
#             change_factor = df.loc[calc_idx, 'ptc_15d']
#             if change_factor == -100:
#                 change_factor = -99
#             base = df.loc[base_idx, 'start_quantity']
#             start_amt = base/(1+(change_factor/100))
#             df.loc[calc_idx, 'start_quantity'] = start_amt
    
        
#         # create figure
#         fig = plt.figure(figsize=(12, 5))
#         X = df.date_start.tolist()
#         Y = df.start_quantity.tolist()
#         plt.plot(X, Y,label=plant)
#         plt.title(f'{county} Covid Waste Water Testing Data from {first_day} to {last_day}')
#         plt.xlabel('Date')
#         plt.ylabel('Viral Load (not to actual scale)')
#         plt.legend()
#         plt.xticks(rotation=70)
