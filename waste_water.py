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
df = df[['wwtp_jurisdiction',  'county_names',  'date_start', 'date_end', 'ptc_15d']]
df.date_start = pd.to_datetime(df.date_start, format='%Y-%m-%d')
df.date_end = pd.to_datetime(df.date_end, format='%Y-%m-%d')
df.sort_values('date_end',inplace=True,axis=0)
df.reset_index(inplace=True,drop=True)
df.loc[0,'quantity'] = 100
print(df)

#see if there's enough data
end_dates = df.date_end.tolist()
start_dates=df.date_start.tolist()
enough = False
for dat in end_dates:
    if dat in start_dates:
        enough = True

if enough:
    print('The starting date has caught up to the first end date.')
else:
    print('There is not yet enough data to begin an analysis')



# x = np.array(df.date_end)
# y = np.array(df.ptc_15d)
# plt.plot(x,y)