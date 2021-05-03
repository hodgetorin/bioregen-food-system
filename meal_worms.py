# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 22:16:49 2021

@author: Owner
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter


#user inputs
n_days = 365 #days
n_crew = 3
mw_space = 20
mw_start_pop = 0
mw_eggs_start = 10000
mw_beetle_start = 0
mw_larvae_start = 0

#constants from csv
mw_survival = 0.75
mw_growth_time = 125
calories_per_mw = 2.06*0.1
protein_per_mw = 0.491*0.1
carbs_per_mw = 0.031*0.1
fats_per_mw = 0.35*0.1
harvest_1 = 850
harvest_2 = 2500
mw_per_sqft = 500


#variables
mw_possible = mw_per_sqft*mw_space

#arrays
mw_pop = np.zeros(n_days)
mw_pop[0] = mw_start_pop

mw_eggs = np.zeros(n_days)
mw_eggs[0] = mw_eggs_start

mw_beetles = np.zeros(n_days)
mw_beetles[0] = mw_beetle_start

mw_larvae = np.zeros(n_days)
mw_larvae[0] = mw_larvae_start

mw_harvest = np.zeros(n_days)
mw_total = np.zeros(n_days)
mw_cumulative = np.zeros(n_days)
t = np.linspace(1,n_days,n_days)

#micronutrient arrays
mw_calories = np.zeros(n_days)
mw_protein = np.zeros(n_days)
mw_carbs = np.zeros(n_days)
mw_fats  =np.zeros(n_days)


# first 2 weeks: eggs hatch
for m in range (1,21):
        mw_eggs[m] = mw_eggs[m-1]-(mw_eggs_start*(0.1))
        mw_pop[m] = 0
        mw_larvae[m] = 0
        mw_beetles[m] = 0
#weeks 3-14: mealworms growing
for m in range (21,105):
        mw_eggs[m] = 0
        mw_pop[m] = mw_eggs[14]
        mw_larvae[m] = 0
        mw_beetles[m] = 0
#weeks 15-22: mealworms ready for harvest
for m in range (105,161):
        mw_eggs[m] = 0
        mw_pop[m] = mw_pop[m-1]-harvest_1
        mw_harvest[m] = mw_harvest[m]+harvest_1
        mw_larvae[m] = 0
        mw_beetles[m] = 0
#weeks 23-24: mealworms in larval stage
for m in range (161,175):
        mw_eggs[m] = 0
        mw_pop[m] = 0
        mw_larvae[m] = mw_pop[154]
        mw_beetles[m] = 0
#weeks 25-37: beetles living and reproducing
for m in range (175,266):
        mw_beetles[m] = mw_larvae[168]

#cycle 2
eggs_per_week = 0.5*mw_beetles[m-1]*6
eggs_hatching = eggs_per_week*0.1
mw_eggs[189] = mw_eggs[m-1]+eggs_hatching

for m in range (196,297,14):
    mw_eggs[m] = mw_eggs[m-1]+eggs_hatching
    mw_eggs[m+1] = mw_eggs[m]-eggs_hatching
   
for m in range (203,287):
    mw_pop[m] = mw_pop[m-1]+eggs_hatching

for m in range (287,n_days):
     mw_pop[m] = mw_pop[m-1]-harvest_2
     mw_harvest[m] = mw_harvest[m]+harvest_2
     mw_larvae[m] = 0
     mw_beetles[m] = 0
     
#all the egs have hatched     
for m in range (287,n_days):
     mw_eggs[m] = 0

#calculate totals     
for m in range (0,n_days):
    mw_total[m] = mw_eggs[m]+mw_larvae[m]+mw_pop[m]+mw_beetles[m]
    mw_cumulative[m] = mw_cumulative[m-1]+mw_total[m]
    #calories and macronutrients
    mw_calories[m] = calories_per_mw*mw_harvest[m]

for j in range (0,n_days):
    if mw_pop[j] > mw_possible:
        mw_pop[j] = mw_possible


print(mw_possible)

plt.plot(t,mw_pop,t,mw_eggs,t,mw_larvae,t,mw_beetles)
plt.legend(['mealworm population','mealworm egg population','larvae population','adult beetle population'], loc = 'upper left') 
plt.ylabel("population"); plt.xlabel("days")
plt.show()
plt.close()
 
plt.plot(t,mw_pop,t,mw_harvest)  
plt.legend(['mealworm population','mealworms harvested'])
plt.ylabel("population"); plt.xlabel("days")  
plt.show()
plt.close()
  
plt.plot(t,mw_total)
plt.legend(['total mealworms in all life stages',])
plt.ylabel("total population"); plt.xlabel("days")
plt.show()
plt.close()

plt.plot(t,mw_cumulative)  
plt.legend(['cumulative mealworms harvested'])
plt.ylabel("population"); plt.xlabel("days")  
plt.show()
plt.close()

plt.plot(t,mw_calories)  
plt.legend(['calories from mealworms'])
plt.ylabel("calories"); plt.xlabel("days")  
plt.show()
plt.close()
