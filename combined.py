# Combined Final

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## Main ##
n_days = 365
n_crew = 8

############################
##   Initializing Plants  ##
############################

# H --> Days until maturation/days until harvest
H_su = 100 # sunflowers
H_sp = 42 # spinach
H_qu = 100 # quinuoa 

# HI --> harvest indexes: % of plant biomass that is edible
HI_su = 0.4 # sunflowers
HI_sp = 0.9 # spinach
HI_qu = 0.3 # quinuoa

# GA --> Growing area; GD --> Growing density
GA_su = 1 # m^2
GD_su = 60000 # g/m^2

GA_sp = 7 
GD_sp = 90*400 

GA_qu = 12
GD_qu = 90*900

# Arrays:
# edible plant mass:
p_ed_su = np.zeros(n_days) # sunflowers
p_ed_sp = np.zeros(n_days) # spinach
p_ed_qu = np.zeros(n_days) # quinoua 

# inedible plant mass:
p_ined_su = np.zeros(n_days) # sunflowers
p_ined_sp = np.zeros(n_days) # spinach
p_ined_qu = np.zeros(n_days) # quinoua 

# total biomass:
p_su = np.zeros(n_days) # sunflowers
p_sp = np.zeros(n_days) # spinach
p_qu = np.zeros(n_days) # quinoua

# total inedible plant mass
p_ined = np.zeros(n_days)


################################
##   Initializing Mushrooms   ##
################################

m_ed = np.zeros(n_days) # edible mushrooms produced 
m_blocks = np.zeros(n_days) # number of substrate blocks
sms = np.zeros(n_days) # spent mushroom substrate mass (g)
m_lc = np.zeros(n_days) # liquid culture per day
#min_sub_to_start = 1000 # placeholder value. need 1000g inedible mass to start a mushroom run

##################
## Main Program ##
##################

for i in range(1,n_days):
    
    # Plants:
    if i % H_su == 0: # harvest sunflowers and quinoa every 100 days
        p_su[i] = GA_su * GD_su # total biomass = growing area * growing density
        p_ed_su[i] = p_su[i] * HI_su # edible sunflower mass
        p_ined_su[i] = (1-HI_su)*p_su[i] # inedible sunflower mass
        
        p_qu[i] = GA_qu * GD_qu # total biomass = growing area * growing density
        p_ed_qu[i] = p_qu[i] * HI_qu # edible quinoa mass
        p_ined_qu[i] = (1-HI_qu)*p_qu[i] # inedible quinoa mass
        
    if i % H_sp == 0: # Harvest spinach every 42 days
        p_sp[i] = GA_sp * GD_sp # Total biomass = Growing area * growing density
        p_ed_sp[i] = p_sp[i] * HI_sp # edible mass
        p_ined_su[i] = (1-HI_su)*p_su[i] # inedible mass
        
    
    if i % 5 == 0: # every 5 days:
        m_blocks[i] = 4 # assuming BE = 100%, mushroom mass == inedible plant mass, harvested 30 days later
        m_lc[i] = 2.5 * 4 # 10 mL of liquid culture used to innoculate bags
    
    # Sum the inedible plant mass:
    p_ined[i] = p_ined_su[i] + p_ined_sp[i] + p_ined_qu[i]
    
    if i % 28 == 0: # every 28 days:
        m_ed[i] = 680 # every 28 days, crew can harvest 680g mushrooms
        m_blocks[i] = -4 # 4 blocks become spent and are no longer producing
        sms[i] = (1082.5 - 680) * 4 # the mass of spent substate equals the difference in substrate input minus fresh wt harvested

# calculate cumulative sums:
m_ed_series = pd.Series(m_ed)
p_ed_su_series = pd.Series(p_ed_su)
p_ed_sp_series = pd.Series(p_ed_sp)
p_ed_qu_series = pd.Series(p_ed_qu)

m_cumsum = m_ed_series.cumsum()
p_ed_su_cumsum = p_ed_su_series.cumsum()
p_ed_sp_cumsum = p_ed_sp_series.cumsum()
p_ed_qu_cumsum = p_ed_qu_series.cumsum()

# time array for plotting:
t = np.linspace(1,n_days,n_days)

# convert from g to kg:
for i in range(n_days):
    p_ed_su[i] = p_ed_su[i]/1000
    p_ed_sp[i] = p_ed_sp[i]/1000
    p_ed_qu[i] = p_ed_qu[i]/1000
    m_ed[i] = m_ed[i]/1000
    
plt.plot(t, p_ed_su, "b-", t, p_ed_sp, "g-", t, p_ed_qu, "p-", t, m_ed, "r-")
plt.title("Food produced over time")
plt.xlabel("time (days)"); plt.ylabel("food produced (kg)")
plt.legend(["Sunflowers", "Spinach", "Quinoa", "Mushrooms"], loc="best")   

plt.plot(t, p_ed_su_cumsum, "b-", t, p_ed_sp_cumsum, "g-", t, p_ed_qu_cumsum, "p-", t, m_cumsum, "r-")
plt.title("Food produced over time (cumulative)")
plt.xlabel("time (days)"); plt.ylabel("food produced (kg)")
plt.legend(["Sunflowers", "Spinach", "Quinoa", "Mushrooms"], loc="best")   
