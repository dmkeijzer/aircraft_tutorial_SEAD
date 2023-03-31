#----------------- Weights and shit -----------------------------------

Oew = 13600 # kg - operative empy weight before modificatons
Zfm = 21000 # kg - zero fuel mass before modifications
Mtwo = 23000 # kg - max take off weight before modifications
Mpl = 7400 # kg - max playload mass before modifications
Mfuel = 5000 # kg - max fuel mass before modfications

#------------ performance -------------------------------------------

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
