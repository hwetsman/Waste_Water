#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 08:28:11 2022

@author: howardwetsman
"""
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt


url = 'https://data.cdc.gov/resource/2ew6-ywp6.json'
data = requests.get(url)
df = pd.read_json(data.content)
print(df)

df.date_start = pd.to_datetime(df.date_start, format='%Y-%m-%d')
df.date_end = pd.to_datetime(df.date_end, format='%Y-%m-%d')
df.sort_values('date_end', inplace=True, axis=0)
print(df.date_end.tolist())
plt.hist(df.date_end)








#