
from atr import *
from const_mod import *

def cg_modification():

    front_bat_weight = 400*g
    back_bat_weight = 800*g

    front_cargo_dist = 2.5922 # meter
    back_cargo_weight = 21.912 # meter
    cargo_dist = [front_cargo_dist, back_cargo_weight]

    cg_OEW, cg_OEW_leamc, OEW, PW = cg_calculation(MTOW, x_lemac)
    cg_OEW_mod = (OEW*cg_OEW + front_cargo_dist*front_cargo_dist + back_bat_weight*back_cargo_weight)/(OEW + front_bat_weight + back_bat_weight)

    return cg_OEW_mod 