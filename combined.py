# Combined Final

# -*- coding: utf-8 -*-
"""
Created on Sun May  2 19:28:39 2021

@author: Torin
"""
  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Database access:
file_in="blss_data.csv"
df = pd.read_csv(file_in)

## Main ##
n_days = int(df.iloc[0][0])
n_crew = int(df.iloc[1][0])

# micronutrient requirements 
ideal_calories = np.zeros(n_days)
ideal_protein = np.zeros(n_days)
ideal_carbs = np.zeros(n_days)
ideal_fats  =np.zeros(n_days)


############################
##   Initializing Plants  ##
############################

# H --> Days until maturation/days until harvest
H_su = int(df.iloc[16][0]) # sunflowers
H_sp = int(df.iloc[10][0]) # spinach
H_qu = int(df.iloc[22][0]) # quinoa 

# HI --> harvest indexes: % of plant biomass that is edible
HI_su = df.iloc[15][0] # sunflowers
HI_sp = df.iloc[9][0] # spinach
HI_qu = df.iloc[21][0] # quinoa

# GA --> Growing area; GD --> Growing density
GA_su = int(df.iloc[25][0]) # m^2
GD_su = int(df.iloc[26][0]) # g/m^2

GA_sp = int(df.iloc[23][0]) 
GD_sp = int(df.iloc[24][0]) 

GA_qu = int(df.iloc[27][0])
GD_qu = int(df.iloc[28][0])

# Arrays:
# edible plant mass:
plant_ed_su = np.zeros(n_days) # sunflowers
plant_ed_sp = np.zeros(n_days) # spinach
plant_ed_qu = np.zeros(n_days) # quinoa 

# inedible plant mass:
plant_ined_su = np.zeros(n_days) # sunflowers
plant_ined_sp = np.zeros(n_days) # spinach
plant_ined_qu = np.zeros(n_days) # quinoa 

# total biomass:
plant_su = np.zeros(n_days) # sunflowers
plant_sp = np.zeros(n_days) # spinach
plant_qu = np.zeros(n_days) # quinoa

# total plant mass
plant_ined = np.zeros(n_days) # inedible
plant_ed = np.zeros(n_days)   # edible

# caloric breakdown:
plant_calories = np.zeros(n_days)
plant_carb = np.zeros(n_days)
plant_pro = np.zeros(n_days)
plant_fat = np.zeros(n_days)

################################
##   Initializing Mushrooms   ##
################################

# Arrays:
shroom_ed = np.zeros(n_days) # edible mushrooms produced 
sms = np.zeros(n_days) # spent mushroom substrate mass (g)
shroom_lc = np.zeros(n_days) # liquid culture per day
shroom_calories = np.zeros(n_days)
shroom_pro = np.zeros(n_days)
shroom_carb = np.zeros(n_days)
shroom_fat = np.zeros(n_days)
#min_sub_to_start = 1000 # placeholder value. need 1000g inedible mass to start a mushroom run

# Constants:
shroom_GA = int(df.iloc[31][0]) # m^2 space required per 4 mushroom blocks

############################
## Initializing Mealworms ##
############################

# arrays:
mw_pop = np.zeros(n_days)
mw_eggs = np.zeros(n_days)
mw_beetles = np.zeros(n_days)
mw_pupae = np.zeros(n_days)

mw_harvest = np.zeros(n_days)
mw_total = np.zeros(n_days)
mw_cumulative = np.zeros(n_days)

weeks = np.linspace(0,n_days,n_days)

# micronutrient breakdown
mw_calories = np.zeros(n_days)
mw_protein = np.zeros(n_days)
mw_carbs = np.zeros(n_days)
mw_fats  =np.zeros(n_days)

# time constants:
mw_survival = int(df.iloc[49][0])
t_egg = int(df.iloc[43][0])
t_larvae = int(df.iloc[44][0])
t_harvest = int(df.iloc[45][0])
t_pupae = int(df.iloc[46][0])
t_beetles = int(df.iloc[47][0])
t_breed = int(df.iloc[48][0])

# for loop
mw_space = 20
mw_start_pop = int(df.iloc[39][0])
mw_eggs_start = int(df.iloc[38][0])
mw_beetle_start = int(df.iloc[40][0])
mw_pupae_start = int(df.iloc[39][0])

# micronutrient breakdown
calories_per_mw = df.iloc[50][0]
protein_per_mw = df.iloc[51][0]
carbs_per_mw = df.iloc[52][0]
fats_per_mw = df.iloc[53][0]

# constants:
harvest_1 = 850
harvest_2 = 2500
mw_GD = int(df.iloc[41][0]) #  growing density per sq ft

# initial values:
mw_pop[0] = mw_start_pop
mw_eggs[0] = mw_eggs_start
mw_pupae[0] = mw_pupae_start
mw_beetles[0] = mw_beetle_start

# mw_max_capacity = mw_per_sqft*mw_space i/t/o GA, GD?



#######################
## Initializing Fish ##
#######################

fish_eggs = np.zeros(n_days)
fish_feed = np.zeros(n_days)
fish_pop = np.zeros(n_days)
fish_meat = np.zeros(n_days)

fish_calories = np.zeros(n_days)
fish_carb = np.zeros(n_days)
fish_pro = np.zeros(n_days)
fish_fat = np.zeros(n_days)

fish_eggs[0] = 600 # starting eggs
fish_pop[0] = int(df.iloc[57][0]) # starting fish

survival_rate = df.iloc[60][0] # survival rate from egg to maturity
growth_time = int(df.iloc[59][0]) # 183 days to grow to maturity?
days_eggs = 56  # counter for cycles (new fish every 56 days)

avg_weight = df.iloc[61][0] # kg average weight of a fish?
amount_feed = df.iloc[62][0]  # the fish is eating 2% of its bodyweight

fish_cals = df.iloc[63][0] # cal/kg?
fish_protein = df.iloc[64][0] #? g/kg? 
fish_carbs = df.iloc[65][0]
fish_fats = df.iloc[66][0]


##################
## Main Program ##
##################


###############################
## Plant and Mushroom Loops: ##
###############################

for i in range(1,n_days):
    
    ## for harvests every 100, 50,... days: average out the harvest over a daily output
    
    # Plants:
    if i % H_su == 0: # harvest sunflowers and quinoa every 100 days
        plant_su[i] = GA_su * GD_su # total biomass = growing area * growing density
        plant_ed_su[i] = plant_su[i] * HI_su # edible sunflower mass
        plant_ined_su[i] = (1-HI_su)*plant_su[i] # inedible sunflower mass
        
        plant_qu[i] = GA_qu * GD_qu # total biomass = growing area * growing density
        plant_ed_qu[i] = plant_qu[i] * HI_qu # edible quinoa mass
        plant_ined_qu[i] = (1-HI_qu)*plant_qu[i] # inedible quinoa mass
        
        plant_ed[i] = plant_ed_qu[i] + plant_ed_su[i]
        
    if i % H_sp == 0: # Harvest spinach every 42 days
        plant_sp[i] = GA_sp * GD_sp # Total biomass = Growing plant_edg area * growing density
        plant_ed_sp[i] = plant_sp[i] * HI_sp # edible mass
        plant_ined_su[i] = (1-HI_su)*plant_su[i] # inedible mass
        
        
    # Sum the inedible plant mass:
    plant_ined[i] = plant_ined_su[i] + plant_ined_sp[i] + plant_ined_qu[i]
    plant_ed[i] = plant_ed_su[i]+plant_ed_sp[i]+plant_ed_qu[i]
    
    plant_calories[i] = 0.23*plant_sp[i] + 6.25*plant_su[i] + 3.68*plant_qu[i]
    plant_carb[i] = .036*plant_sp[i] + .15*plant_su[i] + 3.68*plant_qu[i]
    plant_pro[i] = .0286*plant_sp[i] + .225*plant_su[i] + .1412*plant_qu[i]
    plant_fat[i] = 0.0039*plant_sp[i] + .575*plant_su[i] + .0607*plant_qu[i]
    
    
    
    if (sum(plant_ined) >= 9090): # once there is enough plant waste to produce 4, 5# bags:
        for j in range(i,i+28): # every 28 days, crew can harvest 680g mushrooms. we ration this out across 28 days.
            shroom_ed[j] = 680/28
            shroom_calories[j]=shroom_ed[j]*0.33
            shroom_carb[i]=shroom_ed[j]*0.0609
            shroom_pro[i]=shroom_ed[j]*0.0331
            shroom_fat[i]=shroom_ed[j]*0.0041

        sms[i] = (1082.5 - 680) * 4 # the mass of spent substate equals the difference in substrate input minus fresh wt harvested
        plant_ined[i] = -9090 # use up 9090g of inedible plant mass 
    

#######################
### Mealworm Cycles ###
#######################

# LIMITING FACTORS
#variables
mw_possible_1 = mw_GD*mw_space
mw_possible_2 = sum(sms/(250/150))
if (mw_possible_1 < mw_possible_2):
    mw_possible = mw_possible_1
else:
    mw_possible = mw_possible_2
    
    # first 2 weeks: eggs hatch
for m in range (1,21):
        mw_eggs[m] = mw_eggs[m-1]*0.987
        mw_pop[m] = 0
        mw_pupae[m] = 0
        mw_beetles[m] = 0
        if mw_pop[m] < 0: mw_pop[m] = 0
        if mw_eggs[m] < 0: mw_eggs[m] = 0
        if mw_pupae[m] < 0: mw_pupae[m] = 0
        if mw_beetles[m] < 0: mw_beetles[m] = 0
 #weeks 3-14: mealworms growing
for m in range (21,105):
        mw_eggs[m] = 0
        mw_pop[m] = mw_eggs[20]
        mw_pupae[m] = 0
        mw_beetles[m] = 0
        if mw_pop[m] < 0: mw_pop[m] = 0
        if mw_eggs[m] < 0: mw_eggs[m] = 0
        if mw_pupae[m] < 0: mw_pupae[m] = 0
        if mw_beetles[m] < 0: mw_beetles[m] = 0
#weeks 15-22: mealworms ready for harvest
for m in range (105,161):
        mw_eggs[m] = 0
        mw_pop[m] = mw_pop[m-1]-harvest_1
        mw_harvest[m] = mw_harvest[m]+harvest_1
        mw_pupae[m] = 0
        mw_beetles[m] = 0
        if mw_pop[m] < 0: mw_pop[m] = 0
        if mw_eggs[m] < 0: mw_eggs[m] = 0
        if mw_pupae[m] < 0: mw_pupae[m] = 0
        if mw_beetles[m] < 0: mw_beetles[m] = 0
#weeks 23-24: mealworms in larval stage
for m in range (161,175):
        mw_eggs[m] = 0
        mw_pop[m] = 0
        mw_pupae[m] = mw_pop[142]
        mw_beetles[m] = 0
        if mw_pop[m] < 0: mw_pop[m] = 0
        if mw_eggs[m] < 0: mw_eggs[m] = 0
        if mw_pupae[m] < 0: mw_pupae[m] = 0
        if mw_beetles[m] < 0: mw_beetles[m] = 0
#weeks 25-37: beetles living and reproducing
for m in range (175,265):
        mw_beetles[m] = mw_pupae[174]
        if mw_pop[m] < 0: mw_pop[m] = 0
        if mw_eggs[m] < 0: mw_eggs[m] = 0
        if mw_pupae[m] < 0: mw_pupae[m] = 0
        if mw_beetles[m] < 0: mw_beetles[m] = 0

#beetles reproducing   
for r in range (183,n_days):
        mw_beetles[r] = mw_beetles[r-1]*0.99
        mw_beetles[183] = 0
        mw_eggs[r] = mw_eggs[r-1]+(mw_beetles[r-14]*5/2)-(mw_beetles[r-28]*5/2)
        mw_eggs[183+14] = 0
        if mw_eggs[r] < 0:
            mw_eggs[r] = 0
            
        mw_pop[r] = mw_pop[r-1]+mw_eggs[r-14]
        if r < n_days-84:
            mw_harvest[r+84] = mw_pop[r]
        
#print (mw_eggs[184]-mw_eggs[183])    

#calculate totals     
for m in range (0,n_days):
    mw_total[m] = mw_eggs[m]+mw_pupae[m]+mw_pop[m]+mw_beetles[m]
    mw_cumulative[m] = mw_cumulative[m-1]+mw_total[m]
    #calories and macronutrients
    mw_calories[m] = calories_per_mw*mw_harvest[m]
    mw_protein[m] = protein_per_mw*mw_harvest[m]
    mw_carbs[m] = carbs_per_mw*mw_harvest[m]
    mw_fats[m] = fats_per_mw*mw_harvest[m]
    

for j in range (0,n_days):
    if mw_pop[j] > mw_possible:
        mw_pop[j] = mw_possible
        
mw_eggs = mw_eggs.astype(int)
mw_pop = mw_pop.astype(int)
mw_beetles = mw_beetles.astype(int)
mw_pupae = mw_pupae.astype(int)


###################
### Fish Cycles ###
###################

# limiting factor:
# feed_requirement = avg_weight * grown_fish * amount_feed # how much feed we need to keep fish alive in kg

for i in range(1,n_days):
    
    
    if i % days_eggs == 0: # every 56 days, we get 600 more eggs
        fish_eggs[i]=600 
        
    for j in range(i+35, n_days):
        fish_pop[j] = fish_eggs[i] / (n_days-j)     # hatched eggs turn into baby fish  
        fish_eggs[j] = -fish_pop[j]                 # subtract the hatched eggs
        
        if (j >= growth_time):
            fish_meat[j] = avg_weight * n_crew * 1000 ## harvests 1 fish per person, convert to grams
            fish_pop[i] = -n_crew ## fish population reduces by 1 per crew member
            fish_feed[i] = sum(mw_pop[0:i] - (amount_feed*n_crew)) # 
                
    fish_calories[i] = fish_cals * fish_meat[i]
    fish_carb[i] = fish_carbs * fish_meat[i]
    fish_pro[i] = fish_protein * fish_meat[i]
    fish_fat[i] = fish_fats * fish_meat[i]
        

############################################

for i in range(1,n_days):
    shroom_ed[i] = shroom_ed[i] * 1000 ## scale up mushrooms so they are visible on graphs

# calculate cumulative sums:
shroom_series = pd.Series(shroom_ed)
plant_ed_series = pd.Series(plant_ed)
fish_series = pd.Series(fish_meat)

shroom_cumsum = shroom_series.cumsum()
plant_ed_cumsum = plant_ed_series.cumsum()
fish_cumsum = fish_series.cumsum()

# to calculate 7-day simple moving averages if desired: 
shroom_sma = shroom_series.rolling(7).mean()

##############
## Figures ###
##############

time = np.linspace(1, n_days, n_days)
    
f0 = plt.figure(0)    
plt.plot(time, plant_ed_su, time, plant_ed, time, plant_ed_qu, time, shroom_ed, time,mw_pop, time, fish_meat)
plt.title("Food produced over time")
plt.xlabel("time (days)"); plt.ylabel("food produced (g)")
plt.legend(["Sunflowers", "Spinach", "Quinoa", "Mushrooms x 10^-3", "Mealworms", "Tilapia"], loc="best")   
f0.show()

f1 = plt.figure(1)
plt.plot(time, plant_ed_cumsum, "g-", time, shroom_cumsum, "r-",
         time, mw_cumulative, "k-", time, fish_cumsum, "b-")
plt.title("Total Food Produced During Mission")
plt.xlabel("time (days)"); plt.ylabel("food produced (g)")
plt.legend(["Edible Plant Mass", "Mushrooms", "Mealworms", "Tilapia"], loc="best")   
f1.show()

f2 = plt.figure(2)
plt.plot(weeks,)  #
plt.legend(['cumulative mealworms harvested'])
plt.ylabel("population"); plt.xlabel("days")  
f2.show()

 
plt.plot(time,mw_calories, time, fish_calories, time, shroom_calories, time, plant_calories)  
plt.legend(['mealworms', 'fish', 'mushrooms', 'plants'])
plt.title("Calories produced over time")
plt.ylabel("calories"); plt.xlabel("days")  
plt.show()
