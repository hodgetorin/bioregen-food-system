# Combined Final

import numpy as np
import matplotlib.pyplot as plt

## Main ##
n_days = 365
n_crew = 8

## Initializing Plants (This version: Sunflowers only) ##

# H --> Days until maturation/days until harvest
H_su = 100

# HI --> harvest indexes: % of plant biomass that is edible
HI_su = 0.4

# GA --> Growing area; GD --> Growing density
GA_su = 1 # m^2
GD_su = 60000 # g/m^2

p_ed_su = np.zeros(n_days)
p_ined_su = np.zeros(n_days)

p_su = np.zeros(n_days) 
p_ined = np.zeros(n_days)

p_su[0] = 0 # biomass of entire sunflower plants [g]
p_su_kcal = 6.25 # sunflower seeds calories [kcal/g]



## Initializing Mushrooms ##
m_ed = np.zeros(n_days)
min_sub_to_start = 1000 # placeholder value. need 1000g inedible mass to start a mushroom run


## Main loop ##

for i in range(n_days):
    if i % H_su == 0: # Harvest sunflowers every 100 days
        p_su[i] = GA_su * GD_su # Growing area * growing density 
        
    p_ed_su[i] = p_su[i] * HI_su
    p_ined_su[i] = (1-HI_su)*p_su[i] # inedible sunflower mass produced per day 
    
    # Sum the inedible plant mass:
    p_ined[i] = p_ined_su[i] # + p_ined_sp[i] + ... 
    
    if sum(p_ined) >= min_sub_to_start:
        if i<=(n_days-31):
            m_ed[i+30] = p_ined[i] # assuming BE = 100%, mushroom mass == inedible plant mass, harvested 30 days later


# time array for plotting:
t = np.linspace(1,n_days,n_days)

# convert from g to kg:
for i in range(n_days):
    p_ed_su[i] = p_ed_su[i]/1000
    m_ed[i] = m_ed[i]/1000
    
plt.plot(t, p_ed_su, "b-", t, m_ed, "r--")
plt.title("Food produced over time")
plt.xlabel("time (days)"); plt.ylabel("food produced (kg)")
plt.legend(["Sunflowers", "Mushrooms"], loc="best")
