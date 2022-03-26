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


url = 'https://data.cdc.gov/resource/2ew6-ywp6.json?county_names=Orleans'
data = requests.get(url)
df = pd.read_json(data.content)



df = df[['wwtp_id', 'county_names',  'date_start', 'date_end', 'ptc_15d']]
df = df[~df.ptc_15d.isna()]
df.date_start = pd.to_datetime(df.date_start, format='%Y-%m-%d')
df.date_end = pd.to_datetime(df.date_end, format='%Y-%m-%d')
df.sort_values('date_end', inplace=True, axis=0)
df.reset_index(inplace=True, drop=True)
plants = list(set(df.wwtp_id.tolist()))

start_dates = df.date_start.tolist()
first_day = str(np.array(start_dates).min()).split(' ')[0]

plant_dict = {}
for plant in plants:
    plant_dict[plant] = df[df.wwtp_id == plant]



for plant in plant_dict:
    df = plant_dict.get(plant)
    df.reset_index(drop=True, inplace=True)
    # see if there's enough data
    end_dates = df.date_end.tolist()
    start_dates = df.date_start.tolist()
    first_day = str(np.array(start_dates).min()).split(' ')[0]
    last_day = str(np.array(end_dates).min()).split(' ')[0]
    enough = False
    for dat in end_dates:
        if dat in start_dates:
            enough = True

    # calculate quantity for first end date forward as start
    idx_first = df[df.date_start == df.date_end.min()].index[0]
    for i in range(idx_first, df.index.max()+1, 1):
        if i == idx_first:
            df.loc[i, 'start_quantity'] = 10000
        else:
            base = df.loc[i-1, 'start_quantity']
            percent_change = df.loc[i, 'ptc_15d']
            delta = df.loc[i, 'ptc_15d']/100*base
            new_total = base+delta
            df.loc[i, 'start_quantity'] = int(new_total)

    # infer old values
    to_calculate = df[~df.start_quantity.isna()].date_start.tolist()
    for dat in to_calculate:
        calc_idx = df[df.date_end == dat].index[0]
        base_idx = df[df.date_start == dat].index[0]
        change_factor = df.loc[calc_idx, 'ptc_15d']
        if change_factor == -100:
            change_factor = -99
        base = df.loc[base_idx, 'start_quantity']
        start_amt = base/(1+(change_factor/100))
        df.loc[calc_idx, 'start_quantity'] = start_amt

    
    # create figure
    fig = plt.figure(figsize=(12, 5))
    X = df.date_start.tolist()
    Y = df.start_quantity.tolist()
    plt.plot(X, Y,label=plant)
    plt.title(f'New Orleans Covid Waste Water Testing Data from {first_day} to {last_day}')
    plt.xlabel('Date')
    plt.ylabel('Viral Load (not to actual scale)')
    plt.legend()
    plt.xticks(rotation=70)
