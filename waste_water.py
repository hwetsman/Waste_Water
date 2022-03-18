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
df=pd.read_json(data.content)
df = df[~df.ptc_15d.isna()]
df = df[['county_names',  'date_start', 'date_end', 'ptc_15d']]
df.date_start = pd.to_datetime(df.date_start, format='%Y-%m-%d')
df.date_end = pd.to_datetime(df.date_end, format='%Y-%m-%d')
df.sort_values('date_end',inplace=True,axis=0)
df.reset_index(inplace=True,drop=True)


#see if there's enough data
end_dates = df.date_end.tolist()
start_dates=df.date_start.tolist()
enough = False
for dat in end_dates:
    if dat in start_dates:
        enough = True

#calculate quantity for first end date forward as start
idx_first = df[df.date_start==df.date_end.min()].index[0]
for i in range(idx_first,df.index.max()+1,1):
    if i==idx_first:
        df.loc[i,'start_quantity'] = 10000
    else:
        base = df.loc[i-1,'start_quantity']
        percent_change = df.loc[i,'ptc_15d']
        delta = df.loc[i,'ptc_15d']/100*base
        new_total = base+delta
        df.loc[i,'start_quantity'] = int(new_total)

print(df)


#infer old values
to_calculate = df[~df.start_quantity.isna()].date_start.tolist()
for dat in to_calculate:
    calc_idx = df[df.date_end==dat].index[0]
    base_idx = df[df.date_start==dat].index[0]
    print(calc_idx,base_idx)
print(to_calculate)























# x = np.array(df.date_end)
# y = np.array(df.ptc_15d)
# plt.plot(x,y)