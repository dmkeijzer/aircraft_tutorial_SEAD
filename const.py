import numpy as np
from scipy.constants import g
import latexify

#------------ dimensions -----------------

# wing
s = 61
s_net = s - 7.55
A = 12
cr = 2.57
ct = 1.59
c_mac = 2.11847
b = 27.05
b_half = b/2
taper = ct/cr
y_lemac = (b_half/6) * ((1 + 2*taper)/taper)
x_lemac = 11.60
def convert_lemac(xcg):  return (xcg - x_lemac)/c_mac # just some useful function
xac_bar_w = 0.25

# horizontal tail
s_h = 11.73
b_h = 7.42
A_h = b_h**2/s_h

# xac parameters
h_f = 2.70
l_fn = 11.34
b_f = 2.856 
b_n = 1.00
k_n = -4
l_n = 2.63


# fuselage
l_tot = 27.165

# misc
lh = 14.00
lh_c = lh/c_mac

#deda param
r = lh/b_half
m_tv = 4.15/b_half
phi = np.arcsin(m_tv/r)

#----------------- Weights and shit -----------------------------------

Oew = 13600 # kg - operative empy weight before modificatons
Zfm = 21000 # kg - zero fuel mass before modifications
Mtwo = 23000 # kg - max take off weight before modifications
Mpl = 7400 # kg - max playload mass before modifications
Mfuel = 5000 # kg - max fuel mass before modfications

#------------ performance -------------------------------------------

v_stall = 112*0.5144 # approach speed http://www.independance.pl/atr-speeds.html
w_s_max = 373.8*g # n/m^2
shaft_power = 2750 # horsepower - shaft power 
climb_speed = 170 # KCAS
cruise_speed = 509/3.6 # m/s - 509 at FL170
alt_cruise = 17000*0.3048 # m
rho_cr = 0.721759 #kg/m^3
t_cr = 254.470 #k
mach_at_cruise = cruise_speed/np.sqrt(1.4*287*t_cr) # temperature at FL170 from https://www.digitaldutch.com/atmoscalc/
cl_cr = (2*Mtwo*g)/(rho_cr*cruise_speed**2*s)
fuel_consumption = 650/3600 # kg/s 
one_engine_out_ceiling = 2990 # m / 9800 # ft
max_range_MaxPax = 1370 # km

dict_perf = {'Standard_routes_(NM)': [200, 300, 400],
        'Block_fuel_(kg)': [624, 869, 1115],
        'Block_fuel_(lb)': [1376, 1916, 2458],
        'CO2_emissions_(t)': [1.97, 2.75, 3.52],
        'Block_time(min)': [62, 84, 97]}


#------------ centre of gravity -----------------

cg_w = 12.35
cg_wh = 26.47
cg_wv = 24.15
cg_en = 11.32
cg_fus = 0.39 * l_tot
cg_lm = 12.69
cg_ln = 1.64

#----------------------- Aerodynamics ----------------
@latexify.function
def cl_a_datcom(A,HalfSweep, M=0.4):
        return (2*np.pi*A)/(2 + np.sqrt( 4 + (A*np.sqrt(1 - M**2)/0.95)**2*(1 + np.tan(HalfSweep)**2/(np.sqrt(1 - M**2)))))

@latexify.function
def cl_a_tailles(A,HalfSweep, M=0.4):
        return cl_a_datcom(A, HalfSweep, M)*(1 + 2.15*(b_f/b))*(s_net/s) + np.pi/2*(b_f**2/s)


@latexify.function
def deda_func(r, mtv):
        return (r/(r**2 + mtv**2)*(0.4876/(np.sqrt(r**2 + 0.6319 + mtv**2))) + (1 + (r**2/(r**2 + 0.7915 + 5.0734*mtv**2))**0.3113)*(1 - np.sqrt(mtv**2/(1 + mtv**2))))*(cl_a_datcom(A, 0, mach_at_cruise)/(np.pi*A))

@latexify.function
def deda_prop_add():
        return 6.5*((rho_cr*shaft_power**2*s**3*cl_cr**3)/(lh**4*Mtwo**3))**(1/4)*(np.sin(6*phi))**2.5



# lift coefficients
CL0 = 0.15
CL_tailles_max = w_s_max/(0.5*1.225*v_stall**2)
CL_h_max = -0.35*A_h**(1/3)

# cmac 
cm_ac_airfoil = -0.2 # assummed
cm_ac_w = cm_ac_airfoil*(A/(A + 2))
cm_ac_flaps  = - 0.2 # TODO do it the correct way
cm_ac_fus = -1.8*(1 - (2.5*b_f)/l_tot)*((np.pi*b_f*h_f*l_tot)/(4*s*c_mac))*(CL0/cl_a_tailles(A, 0,  v_stall/np.sqrt(1.4*287*288.15)))
cm_ac = cm_ac_w + cm_ac_fus + cm_ac_flaps


# lift gradient
CL_ah = cl_a_datcom(A_h, np.radians(6), mach_at_cruise) # per radian 
CL_a_tailles =  cl_a_tailles(A, 0, mach_at_cruise)   

# downwash gradient
deda =  deda_func(r, m_tv) + deda_prop_add()

# Aerodynamic centre positions
xac_nacelle_contr = k_n*(b_n**2*l_n)/(s*c_mac*CL_a_tailles)*2 # times two bc thera are two nacelles
xac_bar =  xac_bar_w - 1.8/CL_a_tailles*(b_f*h_f*l_fn)/(s*c_mac) + xac_nacelle_contr # 3rd term ignored since it is 0 anyway due to 0 sweep 

# airspeed reduction
vh_v =   1 # Assume 0.9 is advantage of T-tail is neglibile due to high wing config 