# Combined Final

import numpy as np
import matplotlib.pyplot as plt

## Main ##
n_days = 365
n_crew = 8

## Initializing Plants (This version: Sunflowers only) ##

# harvest indexes: % plant biomass that is edible
HI_su = 0.4

# Growing area
su_GA = 1
su_GD = 6 *10000 

p_ed_su = np.zeros(n_days)
p_ined_su = np.zeros(n_days)

p_su = np.zeros(n_days)
p_ined = np.zeros(n_days)

p_su[0] = 0 # biomass of sunflowers [g]
p_su_kcal = 6.25 #sunflower seeds calories [kcal/g]

H_su = 100 #days til maturation, ready to harvest

## Initializing Mushrooms ##
m_ed = np.zeros(n_days)
min_sub_to_start = 1000 # placeholder value. need 1000g inedible mass to start a mushroom run


## Main loop ##

for i in range(n_days):
    if i % H_su == 0: # Harvest sunflowers every 100 days
        p_su[i] = su_GA * su_GD # Growing area * growing density 
        
    p_ed_su[i] = p_su[i] * HI_su
    p_ined_su[i] = (1-HI_su)*p_su[i] # inedible sunflower mass produced per day 
    
    # Sum the inedible plant mass:
    p_ined[i] = p_ined_su[i] # + p_ined_sp[i] + ... 
    
    if sum(p_ined) >= min_sub_to_start:
        if i<=(n_days-31):
            m_ed[i+30] = p_ined[i] # assuming BE = 100%, mushroom mass == inedible plant mass, harvested 30 days later


# time array for plotting:
t = np.linspace(0,n_days,n_days+1)
    
#plt.plot(t, )




