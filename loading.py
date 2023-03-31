from math import *
import matplotlib.pyplot as plt
import numpy as np

cr = 2.57
ct = 1.59
c_mac = 2.11847
b = 27.05
b_half = b/2
l_tot = 27.165
MTOW = 23000
sweep = 0

taper = ct/cr
y_lemac = (b_half/6) * ((1 + 2*taper)/taper)
print(y_lemac)
x_lemac = 11.60

def cg_calculation(MTOW, x_lemac):
    W_w = 0.149 * MTOW
    W_wh = 0.018 * MTOW
    W_wv = 0.02 * MTOW
    W_en = 0.103 * MTOW
    W_fus = 0.248 * MTOW
    W_lm = 0.035 * MTOW
    W_ln = 0.005 * MTOW
    print("Weights", W_w, W_wh, W_wv, W_en, W_fus, W_lm, W_ln)

    W_fusgroup = W_fus + W_lm + W_ln
    W_wgroup = W_w + W_wh + W_wv + W_en
    W_OEW = W_fusgroup + W_wgroup
    print("Weights of the fuselage, wing and OEW respectively: ", W_fusgroup, W_wgroup, W_OEW)

    cg_w = 12.35
    cg_wh = 26.47
    cg_wv = 24.15
    cg_en = 11.32
    cg_fus = 0.39 * l_tot
    cg_lm = 12.69
    cg_ln = 1.64

    cg_wgroup = (W_w*cg_w + W_wh*cg_wh + W_wv*cg_wv + W_en*cg_en)/W_wgroup
    cg_fusgroup = (W_fus*cg_fus + W_lm*cg_lm + W_ln*cg_ln)/W_fusgroup
    cg_OEW = (W_w*cg_w + W_wh*cg_wh + W_wv*cg_wv + W_en*cg_en + W_fus*cg_fus + W_lm*cg_lm + W_ln*cg_ln)/W_OEW
    print("The center of gravity of fuselage group, wing group, and OEW measured from the nose is: ", cg_fusgroup, cg_wgroup, cg_OEW)

    cg_wgroup_lemac = cg_wgroup - x_lemac
    cg_fusgroup_lemac = cg_fusgroup - x_lemac
    cg_OEW_lemac = cg_OEW - x_lemac
    print("The center of gravity of fuselage group, wing group, and OEW measured from the nose is: ", cg_fusgroup,
          cg_wgroup, cg_OEW)

cg_calculation(MTOW, x_lemac)


