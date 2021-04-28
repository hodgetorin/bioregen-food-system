# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 19:42:35 2021

@author: Torin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file_in="input_mar29.csv"
file_out="output_mar29.csv"

n_days = 365

data = {'time': np.linspace(0, n_days-1, n_days),
        'p_ined': np.zeros(n_days),
        'm_lc': np.zeros(n_days),
        'm_ed': np.zeros(n_days),
        'm_kcal': np.zeros(n_days),
        'm_carb': np.zeros(n_days),
        'm_pro': np.zeros(n_days),
        'm_fat': np.zeros(n_days),
        'sms': np.zeros(n_days),
        }

# convert data into pandas DataFrame:
db = pd.DataFrame(data)

db.m_lc[0] = 1000 # 1000 mL of culture to start

for i in range(1,n_days):
    db.p_ined[i]=145.8 + 655 + 65.6 # produce 866.4g of inedible plant mass every day (sunflowers, quinoa, spinach repectively)
    
# once there is a cumulative                               
for i in range(1,n_days):
    if db.p_ined[i] != 0: # if inedible plant mass was harvested, turn it into mushrooms
        db.m_ed[i+28] = db.p_ined[i] # assuming BE = 100%, mushroom mass == inedible plant mass, harvested 30 days later

for i in range(1,n_days):
    if db.m_ed[i] != 0: # if mushrooms were harvested, convert to macronutrients:
        db.m_kcal[i]=db.m_ed[i]*0.33
        db.m_carb[i]=db.m_ed[i]*0.0609
        db.m_pro[i]=db.m_ed[i]*0.0331
        db.m_fat[i]=db.m_ed[i]*0.0041

print(db)

plt.plot(db.time,db.m_kcal,'b-',db.time,db.m_carb,'r-', db.time,db.m_pro,'k-',db.time,db.m_fat,'g-')
plt.legend(['kcal', 'carbs', 'proteins', 'fats'], loc = 'upper left')
plt.xlabel('day'); plt.ylabel('grams')
plt.show()

db.to_csv(file_out) # save as csv