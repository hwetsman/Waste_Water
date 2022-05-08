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


# select state
# states = ['Louisiana','Florida','Colorado','Idaho']
states = ['Idaho', 'Texas', 'Washington', 'Maine', 'Missouri', 'Illinois', 'New York', 'South Dakota', 'Nebraska', 'Oregon', 'Wisconsin', 'Nevada', 'South Carolina', 'Colorado', 'Minnesota', 'West Virginia',
          'Kansas', 'Michigan', 'Georgia', 'Maryland', 'California', 'Vermont', 'Massachusetts', 'Louisiana', 'Rhode Island', 'Ohio', 'Indiana', 'North Carolina', 'Utah', 'Florida', 'Iowa', 'Connecticut', 'Virginia']
states.sort()
state = st.sidebar.selectbox('State of Interest', states)
# st.write(state)

url = f'https://data.cdc.gov/resource/2ew6-ywp6.json?wwtp_jurisdiction={state}'
data = requests.get(url)
df = pd.read_json(data.content)
df.sort_values('date_end', inplace=True)


df = df[df.reporting_jurisdiction == state]
counties = list(set(df.county_names.tolist()))
counties.sort()
county = st.sidebar.selectbox('County of Interest', counties)

# st.write(county)
df = df[df.county_names == county]
plants = list(set(df.wwtp_id.tolist()))

# st.write(plants)
plant = st.sidebar.selectbox('Treatment Plant', plants)
df = df[df.wwtp_id == plant]

df = df[['wwtp_id', 'county_names',  'date_start', 'date_end', 'ptc_15d']]
df = df[~df.ptc_15d.isna()]
df.reset_index(drop=True, inplace=True)
df.sort_values('date_end', inplace=True, axis=0)
df.drop_duplicates(inplace=True)
# st.write(df)

# get first and last day
# df.date_start = pd.to_datetime(df.date_start, yearfirst=True)
# starting_dates = df.date_start.tolist()
# df.date_end = pd.to_datetime(df.date_end, yearfirst=True)
# ending_dates = df.date_end.tolist()
# st.write(df)
# first_day = str(np.array(starting_dates).min()).split(' ')[0]
first_day = df.loc[14, 'date_start']
last_day = df.loc[df.shape[0]-1, 'date_end']
# last_day = str(np.array(ending_dates).max()).split(' ')[0]
# st.write(first_day, last_day)
# calculate quantity for first end date forward as start

# df.reset_index(inplace=True, drop=True)
idx_first = df[df.date_start == df.date_end.min()].index[0]
start_quant = 1000000
# st.write(idx_first, start_quant)

plotter = pd.DataFrame()
day = df.date_end.tolist()[-1]
while day in df.date_end.tolist():
    idx = df[df.date_end == day].index[0]
    next = next_date = df.loc[idx, 'date_start']
    pct = df.loc[idx, 'ptc_15d']
    plotter.loc[idx, 'ptc'] = pct
    plotter.loc[idx, 'start'] = next
    plotter.loc[idx, 'end'] = day
    day = next
plotter.sort_values('start', inplace=True)
plotter.reset_index(drop=True, inplace=True)
plotter.loc[plotter.index.max()+1, 'end'] = plotter.loc[0, 'start']
plotter.sort_values('end', inplace=True)
plotter.reset_index(drop=True, inplace=True)
for i in plotter.index:
    if i == 0:
        plotter.loc[i, 'quant'] = 1000
    else:
        plotter.loc[i, 'quant'] = max(
            1, int(plotter.loc[i-1, 'quant']*(1+(plotter.loc[i, 'ptc']/100))))

# plot plotter quantitites
fig1, ax1 = plt.subplots()
fig1 = plt.figure(figsize=(20, 8))
Y1 = plotter.quant.tolist()
X1 = pd.to_datetime(plotter.end.tolist())
plt.plot(X1, Y1, label=plant)
plt.yscale('log')
plt.title(
    f'{county} Covid Waste Water Testing Data from {plotter.start.tolist()[1]} to {plotter.end.tolist()[-1]}')
plt.xlabel('Date')
plt.ylabel('Example copy number change over time (not actual quantities)')
plt.legend()
plt.xticks(rotation=70)
st.pyplot(fig1)


# plot df changes
Y = df['ptc_15d'].tolist()

# add figure
fig, ax = plt.subplots()
fig = plt.figure(figsize=(20, 8))
X = pd.to_datetime(df.date_end.tolist())
plt.plot(X, Y, label=plant)

#
plt.title(f'{county} Covid Waste Water Testing Data from {first_day} to {last_day}')
plt.xlabel('Date')
plt.ylabel('% change from 15 days previous')
plt.legend()
plt.hlines(0, X[0], X[-1], colors='black')
plt.xticks(rotation=70)
for index, label in enumerate(ax.xaxis.get_ticklabels()):
    if index % 5 != 0:
        label.set_visible(False)
st.pyplot(fig)


# alternate data source for Orange County
# if state == 'Florida' and county == 'Orange':
#     url = 'https://raw.githubusercontent.com/biobotanalytics/covid19-wastewater-data/6cccf0ee1c4248ece605468096fad2af4bb058b5/wastewater_by_county.csv'
#     df = pd.read_csv(url)
#     df.drop('Unnamed: 0',axis=1,inplace=True)

#     states = ['FL']
#     df = df[df.state.isin(states)]
#     df = df[df.name == 'Orange County, FL']
#     df.sampling_week = pd.to_datetime(df.sampling_week, format='%Y-%m-%d')
#     df = df[['sampling_week','effective_concentration_rolling_average']]
#     fig = plt.figure(figsize=(12, 5))
#     first_day = str(df.sampling_week.min()).split(' ')[0]
#     last_day = str(df.sampling_week.max()).split(' ')[0]

#     fig = plt.figure(figsize=(10,8))
#     X = df.sampling_week.tolist()
#     Y = df.effective_concentration_rolling_average.tolist()
#     plt.plot(X, Y)
#     plt.title(f'Orange County Covid Waste Water Testing Data from {first_day} to {last_day}')
#     plt.xlabel('Date')
#     plt.ylabel('Effective Concentration Rolling Average')
#     plt.legend()
#     plt.yscale('log')
#     plt.xticks(rotation=70)
#     st.pyplot(fig)

# else:
