# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 15:56:46 2021

@author: kate
"""
from numpy import *
import matplotlib.pyplot as plt
#plant run 423 Project BLSS mass balance
# 1300 = 5650g, 400 = 64g, 1600 = 435g

#Plant Nutrient Profiles 
nod = 365 #number of days
noc = 8 #number of crew members
p_sp = zeros(nod) 
p_sp[0] = 0 #biomass of spinach [g]
p_sp_kcal = 0.23 #spinach calories [kcal/g]
p_sp_carb = 0.036 #spinach carbs [g/g]
p_sp_prot = 0.0286 #spinach protein [g/g]
p_sp_fat = 0.0039 #spinach fats [g/g]
H_sp = 42 #day til ready to harvest, can harvest for two weeks

p_su = zeros(nod)
p_su[0] = 0 #biomass of sunflower seeds [g]
p_su_kcal = 6.25 #sunflower seeds calories [kcal/g]
p_su_carb = 0.15 #sunflower seeds carbs [g/g]
p_su_prot = 0.225 #sunflower seeds protein [g/g]
p_su_fat = 0.575 #sunflower seeds fats [g/g]
H_su = 100 #days til maturation, ready to harvest

p_qu = zeros(nod)
p_qu[0] = 0 #biomass of quinoa [g]
p_qu_kcal = 3.68 #quinoa calories [kcal/g]
p_qu_carb = 0.6416 #quinoa carbs [g/g]
p_qu_prot = 0.1412 #quinoa protein [g/g]
p_qu_fat = 0.0607 #quinoa fats [g/g]
H_qu = 100 #days til maturation, ready to harvest

#harvest indexes: % plant biomass that is edible
HI_sp = 0.9 
HI_su = 0.4
HI_qu = 0.3 

sp_GA = 7 #sqm, 
sp_GD = 90*400 #plants per sqm * g per plant
su_GA = 1
su_GD = 6 *10000 
qu_GA = 12
qu_GD = 90*900

for i in range(nod):
    if i % 42 == 0:
        p_sp[i] = sp_GA * sp_GD
    if i % 100 == 0:
        p_su[i] = su_GA * su_GD
        p_qu[i] = qu_GA * qu_GD

#Plant edible mass = food [g/day]
p_ed_sp = p_ed_su = p_ed_qu = zeros(nod)
for i in range(nod):
    p_ed_sp[i] = p_sp[i] * HI_sp
    p_ed_su[i] = p_su[i] * HI_su
    p_ed_qu[i] = p_qu[i] * HI_qu
    
#Nutrient Calculations
kcal = zeros(nod)
carb = zeros(nod)
prot = zeros(nod)
fat = zeros(nod)

for i in range(nod):
    kcal[i] = p_ed_sp[i] * p_sp_kcal + p_ed_su[i] * p_su_kcal + p_ed_qu[i] * p_qu_kcal
    carb[i] = p_ed_sp[i] * p_sp_carb + p_ed_su[i] * p_su_carb + p_ed_qu[i] * p_qu_carb
    prot[i] = p_ed_sp[i] * p_sp_prot + p_ed_su[i] * p_su_prot + p_ed_qu[i] * p_qu_prot
    fat[i] = p_ed_sp[i] * p_sp_fat + p_ed_su[i] * p_su_fat + p_ed_qu[i] * p_qu_fat

time = linspace(1,nod,nod)
plt.plot(time,p_su,'ro', time, p_sp, 'g-', time, p_qu, 'b-')
plt.legend(['sunflowers','spinach', 'quinoa'])
plt.xlabel('number of days'); plt.ylabel('harvested produce in grams')
plt.show()

plt.plot(time, kcal, 'r-', time, carb, 'go-', time, prot, 'bo-', time, fat, 'yo-')
plt.legend(['calories','carbs', 'protein', 'fats'])
plt.xlabel('number of days'); plt.ylabel('nutritional info')
plt.show()
plt.close()

#Plant Growth Factors
PPHD = 16 #photoperiod [hours/day]
PPFD_sp = 295 #photosynthetic photon flux [umol / sqm / s]
PPFD_su = 400 #photosynthetic photon flux [umol / sqm / s]
PPFD_qu = 400 #photosynthetic photon flux [umol / sqm / s]

#identifying Daily Light Integral (DLI = PPFD * PPHD) [mol / sqm/ day]
DLI_sp = PPFD_sp * PPHD
DLI_su = PPFD_su * PPHD
DLI_qu = PPFD_qu * PPHD

#DLI Correction Factors
LABC = 0.9 #percent of light absorbed by canopy 
PSCE = 0.75 #photosynthetic coversion efficiency
PAR = 217 #[kJ/mol] energy of one mol of photosynthetic active radiation

#amt of food energy produced per unit area in a day [kJ / sqm / day]
FEPUAD_sp = DLI_sp * (LABC + PSCE + PAR + HI_sp)
FEPUAD_su = DLI_su * (LABC + PSCE + PAR + HI_su)
FEPUAD_qu = DLI_qu * (LABC + PSCE + PAR + HI_qu)

#Growing Area Calculations
#GA_sp = GA_su = GA_qu = GA_tot = 0
#required growing area = food energy required per crew
#GA_sp = FEPUAD_sp / (p_ed_sp * p_sp_kcal)
#GA_su = FEPUAD_su / (p_ed_su * p_su_kcal)
#GA_qu = FEPUAD_qu / (p_ed_qu * p_qu_kcal)
#want total GA for each crew memeber 20 sqm or less (NASA approved)
#GA_tot = GA_sp + GA_su + GA_qu

#print('kcal:', kcal)
#print('carbs:', carb)
#print('protein:', prot)
#print('fats:', fat)

#print('total GA:', GA_tot) #'GA spinach:', GA_sp, "GA sunflower:", GA_su, "GA quinoa:", GA_qu,
