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



################################
##   Initializing Mushrooms   ##
################################

# Arrays:
shroom_ed = np.zeros(n_days) # edible mushrooms produced 
sms = np.zeros(n_days) # spent mushroom substrate mass (g)
shroom_lc = np.zeros(n_days) # liquid culture per day
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

fish_eggs[0] = 600 # starting eggs
fish_pop[0] = int(df.iloc[57][0]) # starting fish

survival_rate = df.iloc[60][0] # survival rate from egg to maturity
growth_time = int(df.iloc[59][0]) # 183 days to grow to maturity?
days_eggs = 56  # counter for cycles (new fish every 56 days)

avg_weight = df.iloc[61][0] # kg average weight of a fish?
amount_feed = df.iloc[62][0]  # the fish is eating 2% of its bodyweight

fish_cal = int(df.iloc[63][0]) # cal/kg?
fish_prot = df.iloc[64][0] #? g/kg? 
fish_carb = int(df.iloc[65][0])
fish_fat = df.iloc[66][0]
