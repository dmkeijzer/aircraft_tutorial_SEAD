import numpy as np
from scipy.constants import g


#----------------- Weights and shit -----------------------------------

Oew = 13600 # kg - operative empy weight before modificatons
Zfm = 21000 # kg - zero fuel mass before modifications
Mtwo = 23000 # kg - max take off weight before modifications
Mpl = 7400 # kg - max playload mass before modifications
Mfuel = 5000 # kg - max fuel mass before modfications

#------------ performance -------------------------------------------

v_stall = 112*0.5144 # approach speed http://www.independance.pl/atr-speeds.html
w_s_max = 373.8*g # n/m^2
shaft_power = 2022.6217*1e3 # watts - shaft power 
climb_speed = 170 # KCAS
max_cruise_speed = 500/3.6 # m/s 
fuel_consumption = 650/3600 # kg/s 
one_engine_out_ceiling = 2990 # m / 9800 # ft
max_range_MaxPax = 1370 # km

dict_perf = {'Standard_routes_(NM)': [200, 300, 400],
        'Block_fuel_(kg)': [624, 869, 1115],
        'Block_fuel_(lb)': [1376, 1916, 2458],
        'CO2_emissions_(t)': [1.97, 2.75, 3.52],
        'Block_time(min)': [62, 84, 97]}

#------------ dimensions -----------------

s = 61
s_h = 11.73
b_h = 7.42
A_h = b_h**2/s_h
cr = 2.57
ct = 1.59
c_mac = 2.11847
b = 27.05
b_half = b/2
l_tot = 27.165
taper = ct/cr
y_lemac = (b_half/6) * ((1 + 2*taper)/taper)
x_lemac = 11.60
def convert_lemac(xcg):  return (xcg - x_lemac)/c_mac # just some useful function
xac_bar = 0.25 
#------------ centre of gravity -----------------

cg_w = 12.35
cg_wh = 26.47
cg_wv = 24.15
cg_en = 11.32
cg_fus = 0.39 * l_tot
cg_lm = 12.69
cg_ln = 1.64

#----------------------- Aerodynamics ----------------

CL_tailles_max = w_s_max/(0.5*1.225*v_stall**2)
CL_h_max = -0.35*A_h**(1/3)
cm_ac = -0.1
CL_ah = 4.627379968808672 # per radian - taken from svv for now
CL_a_tailles = 4.826827278421984   # for now taken from svv
deda =  0.30 # assumed
lh =   26.21   # Used method from adsee to compute centre of pressure and use this distance
lh_c = lh/c_mac
vh_v =  0.9