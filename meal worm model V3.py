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

n_days = 300 #weeks
astronauts = 3
mw_space = 20
mw_start_pop = 0
mw_eggs_start = 10000
mw_beetle_start = 0
mw_pupae_start = 0

#constants from csv
mw_survival = 0.75
t_egg = 21
t_larvae = 84
t_harvest = 56
t_pupae = 14
t_beetles = 84
t_breed = 14

sms = 100000

calories_per_mw = 2.06*0.1
protein_per_mw = 0.491*0.1
carbs_per_mw = 0.031*0.1
fats_per_mw = 0.35*0.1

harvest_1 = 850
harvest_2 = 2500
mw_per_sqft = 500


#variables
mw_possible_1 = mw_per_sqft*mw_space
mw_possible_2 = sms/250
if mw_possible_1 < mw_possible_2:
    mw_possible = mw_possible_1
else:
    mw_possible = mw_possible_2

#arrays
mw_pop = np.zeros(n_days)
mw_pop[0] = mw_start_pop

mw_eggs = np.zeros(n_days)
mw_eggs[0] = mw_eggs_start

mw_beetles = np.zeros(n_days)
mw_beetles[0] = mw_beetle_start

mw_pupae = np.zeros(n_days)
mw_pupae[0] = mw_pupae_start

mw_harvest = np.zeros(n_days)
mw_total = np.zeros(n_days)
mw_cumulative = np.zeros(n_days)
weeks = np.linspace(0,n_days,n_days)

#micronutrient arrays
mw_calories = np.zeros(n_days)
mw_protein = np.zeros(n_days)
mw_carbs = np.zeros(n_days)
mw_fats  =np.zeros(n_days)


#for m in range (0,n_days):
# first 2 weeks: eggs hatch
for m in range (1,t_egg):
        mw_eggs[m] = mw_eggs[m-7]-(mw_eggs_start*(0.3/2))
        mw_pop[m] = 0
        mw_pupae[m] = 0
        mw_beetles[m] = 0
#weeks 3-14: mealworms growing
for m in range (t_egg,t_harvest+t_egg):
        mw_eggs[m] = 0
        mw_pop[m] = mw_eggs[14]
        mw_pupae[m] = 0
        mw_beetles[m] = 0
#weeks 15-22: mealworms ready for harvest
for m in range (t_harvest+t_egg,t_harvest+t_egg+t_larvae):
        mw_eggs[m] = 0
        mw_pop[m] = mw_pop[m-7]-harvest_1
        mw_harvest[m] = mw_harvest[m]+harvest_1
        mw_pupae[m] = 0
        mw_beetles[m] = 0
#weeks 23-24: mealworms in pupal stage
for m in range (t_harvest+t_egg+t_larvae,t_harvest+t_egg+t_larvae+t_pupae):
        mw_eggs[m] = 0
        mw_pop[m] = 0
        mw_pupae[m] = mw_pop[t_harvest+t_egg+t_larvae+t_pupae-14]
        mw_beetles[m] = 0
#weeks 25-37: beetles living and reproducing
for m in range (t_harvest+t_egg+t_larvae+t_pupae,t_harvest+t_egg+t_larvae+t_pupae+t_beetles):
        mw_beetles[m] = mw_pupae[t_harvest+t_egg+t_larvae+t_pupae-7]

#cycle 2
eggs_per_week = 0.5*mw_beetles[m-1]*40
eggs_hatching = eggs_per_week*0.7
mw_eggs[t_harvest+t_egg+t_larvae+t_pupae+14] = mw_eggs[m-7]+eggs_hatching

for m in range (28,41,2):
    mw_eggs[m] = mw_eggs[m-1]+eggs_hatching
    mw_eggs[m+1] = mw_eggs[m]-eggs_hatching
   
for m in range (29,41):
    mw_pop[m] = mw_pop[m-1]+eggs_hatching

for m in range (41,n_days):
     mw_pop[m] = mw_pop[m-1]-harvest_1
     mw_harvest[m] = mw_harvest[m]+harvest_1
     mw_pupae[m] = 0
     mw_beetles[m] = 0
     
#all the eggs have hatched     
for m in range (41,n_days):
     mw_eggs[m] = 0

#calculate totals     
for m in range (0,n_days):
    mw_total[m] = mw_eggs[m]+mw_pupae[m]+mw_pop[m]+mw_beetles[m]
    mw_cumulative[m] = mw_cumulative[m-1]+mw_total[m]
    #calories and macronutrients
    mw_calories[m] = calories_per_mw*mw_harvest[m]

for j in range (0,n_days):
    if mw_pop[j] > mw_possible:
        mw_pop[j] = mw_possible


print(mw_possible)

plt.plot(weeks,mw_pop,weeks,mw_eggs,weeks,mw_pupae,weeks,mw_beetles)
plt.legend(['mealworm population','mealworm egg population','larvae population','adult beetle population'], loc = 'upper left') 
plt.ylabel("population"); plt.xlabel("days")
plt.show()
plt.close()
 
plt.plot(weeks,mw_pop,weeks,mw_harvest)  
plt.legend(['mealworm population','mealworms harvested'])
plt.ylabel("population"); plt.xlabel("days")  
plt.show()
plt.close()
  
plt.plot(weeks,mw_total)
plt.legend(['total mealworms in all life stages',])
plt.ylabel("total population"); plt.xlabel("days")
plt.show()
plt.close()

plt.plot(weeks,mw_cumulative)  
plt.legend(['cumulative mealworms harvested'])
plt.ylabel("population"); plt.xlabel("days")  
plt.show()
plt.close()

plt.plot(weeks,mw_calories)  
plt.legend(['calories from mealworms'])
plt.ylabel("calories"); plt.xlabel("days")  
plt.show()
plt.close()