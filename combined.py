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


shroom_ed = np.zeros(n_days)
sms = np.zeros(n_days)



############################
##   Initializing Plants  ##
############################

# H --> Days until maturation/days until harvest
H_su = int(df.iloc[16][0]) # sunflowers
H_sp = int(df.iloc[10][0]) # spinach
H_qu = int(df.iloc[22][0]) # quinuoa 

# HI --> harvest indexes: % of plant biomass that is edible
HI_su = int(df.iloc[15][0]) # sunflowers
HI_sp =int(df.iloc[9][0]) # spinach
HI_qu = int(df.iloc[21][0]) # quinuoa

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
plant_ed_qu = np.zeros(n_days) # quinoua 

# inedible plant mass:
plant_ined_su = np.zeros(n_days) # sunflowers
plant_ined_sp = np.zeros(n_days) # spinach
plant_ined_qu = np.zeros(n_days) # quinoua 

# total biomass:
plant_su = np.zeros(n_days) # sunflowers
plant_sp = np.zeros(n_days) # spinach
plant_qu = np.zeros(n_days) # quinoua

# total plant mass
plant_ined = np.zeros(n_days) # inedible
plant_ed = np.zeros(n_days)   # edible



################################
##   Initializing Mushrooms   ##
################################

# Arrays:
shroom_ed = np.zeros(n_days) # edible mushrooms produced 
sms = np.zeros(n_days) # spent mushroom substrate mass (g)
shroom_lc = np.zeros(n_days) # liquid culture per day
#min_sub_to_start = 1000 # placeholder value. need 1000g inedible mass to start a mushroom run

# Constants:
shroom_GA = 0.33 # m^2 space required per 4 mushroom blocks

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
mw_survival = 0.75
t_egg = 21
t_larvae = 84
t_harvest = 56
t_pupae = 14
t_beetles = 84
t_breed = 14

# for loop
mw_space = 20
mw_start_pop = 0
mw_eggs_start = 10000
mw_beetle_start = 0
mw_pupae_start = 0

# micronutrient breakdown
calories_per_mw = 2.06*0.1
protein_per_mw = 0.491*0.1
carbs_per_mw = 0.031*0.1
fats_per_mw = 0.35*0.1

# constants:
harvest_1 = 850
harvest_2 = 2500
mw_GD = 500 #  growing density per sq ft

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

fish_eggs[0] = 600 # starting eggs
fish_pop[0] = 50 # starting fish

survival_rate = 0.75 # survival rate from egg to maturity
growth_time = 183 # 183 days to grow to maturity?
days_eggs = 56  # counter for cycles (new fish every 56 days)

avg_weight = 2.4 # kg average weight of a fish?
amount_feed = 0.02  # the fish is eating 2% of its bodyweight

fish_cal = 98 # cal/kg?
fish_prot = 0.26 #? g/kg? 
fish_carb = 0
fish_fat = 0.025



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
        
    if i % H_sp == 0: # Harvest spinach every 42 days
        plant_sp[i] = GA_sp * GD_sp # Total biomass = Growing area * growing density
        plant_ed_sp[i] = plant_sp[i] * HI_sp # edible mass
        plant_ined_su[i] = (1-HI_su)*plant_su[i] # inedible mass
        
    # Sum the inedible plant mass:
    plant_ined[i] = plant_ined_su[i] + plant_ined_sp[i] + plant_ined_qu[i]
    
    if sum(plant_ined >= 9090): # once there is enough plant waste to produce 4, 5# bags:
        shroom_ed[i] = 680 # every 28 days, crew can harvest 680g mushrooms
        sms[i] = (1082.5 - 680) * 4 # the mass of spent substate equals the difference in substrate input minus fresh wt harvested
        plant_ined[i] = -9090 
        



#######################
### Mealworm Cycles ###
#######################

# LIMITING FACTORS
mw_possible_1 = mw_GD * mw_space # max capacity worms
# spent mushroom substrare limiting
mw_possible_2 = sum(sms)/250     # max capacity worms based on sms (250g sms required)
if mw_possible_1 < mw_possible_2: 
    mw_possible = mw_possible_1
else:
    mw_possible = mw_possible_2

# Mealworm Cycle 1: 

# first 2 weeks: eggs hatch
for m in range (1,t_egg):
        mw_eggs[m] = mw_eggs[m-7]-(mw_eggs_start*(0.3/2))
        mw_pop[m] = 0
        mw_pupae[m] = 0
        mw_beetles[m] = 0
# weeks 3-14: mealworms growing
for m in range (t_egg,t_harvest+t_egg):
        mw_eggs[m] = 0
        mw_pop[m] = mw_eggs[14]
        mw_pupae[m] = 0
        mw_beetles[m] = 0
# weeks 15-22: mealworms ready for harvest
for m in range (t_harvest+t_egg,t_harvest+t_egg+t_larvae):
        mw_eggs[m] = 0
        mw_pop[m] = mw_pop[m-7]-harvest_1
        mw_harvest[m] = mw_harvest[m]+harvest_1
        mw_pupae[m] = 0
        mw_beetles[m] = 0
# weeks 23-24: mealworms in pupal stage
for m in range (t_harvest+t_egg+t_larvae,t_harvest+t_egg+t_larvae+t_pupae):
        mw_eggs[m] = 0
        mw_pop[m] = 0
        mw_pupae[m] = mw_pop[t_harvest+t_egg+t_larvae+t_pupae-14]
        mw_beetles[m] = 0
# weeks 25-37: beetles living and reproducing
for m in range (t_harvest+t_egg+t_larvae+t_pupae,t_harvest+t_egg+t_larvae+t_pupae+t_beetles):
        mw_beetles[m] = mw_pupae[t_harvest+t_egg+t_larvae+t_pupae-7]

# Mealworm Cycle 2
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
    mw_calories[m] = calories_per_mw*mw_harvest[m]   # calories and macronutrients
    
for m in range (0,n_days):
    if mw_pop[m] > mw_possible:
        mw_pop[m] = mw_possible

for m in range(0,n_days):
    mw_pop[m] = mw_pop[m] /10000 # *10^-4
    mw_cumulative[m] = mw_cumulative[m]/10000 

print(mw_possible)


###################
### Fish Cycles ###
###################

#feed_requirement = avg_weight * grown_fish * amount_feed # how much feed we need to keep fish alive in kg

#mw_feed = feed * 0.67 # array of mealworm inputs (67% of total feed)
#mush_feed = feed * 0.33 # sms input

## 1 fish per crewmate per day

for i in range(1,n_days):
    if n_days % days_eggs == 0: # every 56 days, we get more eggs
        fish_eggs[i]=600 
    
    if i % growth_time == 0:
        fish_pop[i] = sum(fish_eggs[n_days-growth_time:n_days]) * 0.75 
        fish_eggs[i] = -sum(fish_eggs[n_days-growth_time:n_days])
        #fish_meat[i] = avg_weight * sum(fish_pop[(n_days-growth_time),n_days])
        

# calculate cumulative sums:
shroom_series = pd.Series(shroom_ed)
plant_ed_su_series = pd.Series(plant_ed_su)
plant_ed_sp_series = pd.Series(plant_ed_sp)
plant_ed_qu_series = pd.Series(plant_ed_qu)
fish_series = pd.Series(fish_pop)

shroom_cumsum = shroom_series.cumsum()
plant_ed_su_cumsum = plant_ed_su_series.cumsum()
plant_ed_sp_cumsum = plant_ed_sp_series.cumsum()
plant_ed_qu_cumsum = plant_ed_qu_series.cumsum()
fish_cumsum = fish_series.cumsum()


# to calculate 7-day simple moving averages if desired: 
shroom_sma = shroom_series.rolling(7).mean()

# convert from g to kg:
#for i in range(n_days):
 #   p_ed_su[i] = p_ed_su[i]/1000
 #   p_ed_sp[i] = p_ed_sp[i]/1000
  #  p_ed_qu[i] = p_ed_qu[i]/1000
  #  m_ed[i] = m_ed[i]/1000



##############
## Figures ###
##############

time = np.linspace(1, n_days, n_days)
    
f0 = plt.figure(0)    
plt.plot(time, plant_ed_su, "b-", time, plant_ed, "g-", time, plant_ed_qu, "c-", time, shroom_ed, "r-")
plt.title("Food produced over time")
plt.xlabel("time (days)"); plt.ylabel("food produced (g)")
plt.legend(["Sunflowers", "Spinach", "Quinoa", "Mushrooms"], loc="best")   
f0.show()

f1 = plt.figure(1)
plt.plot(time, plant_ed_su_cumsum, "b-", time, plant_ed_sp_cumsum, "g-", 
         time, plant_ed_qu_cumsum, "c-", time, shroom_cumsum, "r-",
         time, -mw_cumulative, "k-", time, fish_cumsum, "y-")
plt.title("Total Food Produced During Mission")
plt.xlabel("time (days)"); plt.ylabel("food produced (g)")
plt.legend(["Sunflowers", "Spinach", "Quinoa", "Mushrooms", "Mealworms", "Tilapia"], loc="best")   
f1.show()

f2 = plt.figure(2)
plt.plot(weeks,)  #
plt.legend(['cumulative mealworms harvested'])
plt.ylabel("population"); plt.xlabel("days")  
f2.show()
