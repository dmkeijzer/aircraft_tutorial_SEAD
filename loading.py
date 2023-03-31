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
    print("The center of gravity of fuselage group, wing group, and OEW measured from the lemac is: ", cg_fusgroup,
          cg_wgroup, cg_OEW)

    cg_perc_w = cg_wgroup_lemac/c_mac
    cg_perc_f = cg_fusgroup_lemac/c_mac
    cg_perc_OEW = cg_OEW_lemac/c_mac
    print("The center of gravity of fuselage group, wing group, and OEW measured from the lemac as percentage of mac is: ", cg_perc_w,
          cg_perc_f, cg_perc_OEW)

    return cg_OEW, cg_OEW_lemac,  W_OEW

cg_oew, cg_oew_lemac, OEW= cg_calculation(MTOW, x_lemac, )

def convert_lemac(xcg):
    return (xcg - x_lemac)/c_mac
vec_convert_lemac = np.vectorize(convert_lemac)


def loading_diagrams():
    seat_pitch = np.arange(6, 18.963, 29*0.0254)

    front_cargo = 2.5922 # meter
    back_cargo = 21.912 # meter

    cargo_dist = [front_cargo, back_cargo]

    max_cargo = 7400 # kg
    
    # initiate
    cg_cargo_pot_fb = [cg_oew]
    fb_weight_cargo =  [OEW]

    cg_cargo_pot_bf = [cg_oew]
    bf_weight_cargo =  [OEW]

    # front to back
    for dist in cargo_dist:
        new_xcg = (fb_weight_cargo[-1]*cg_cargo_pot_fb[-1] + max_cargo/2*dist)/(max_cargo/2 + fb_weight_cargo[-1])
        cg_cargo_pot_fb.append(new_xcg)
        fb_weight_cargo.append(fb_weight_cargo[-1] + max_cargo/2)

    # back to front
    for dist in np.flip(cargo_dist):
        new_xcg = (bf_weight_cargo[-1]*cg_cargo_pot_bf[-1] + max_cargo/2*dist)/(max_cargo/2 + bf_weight_cargo[-1])
        cg_cargo_pot_bf.append(new_xcg)
        bf_weight_cargo.append(bf_weight_cargo[-1] + max_cargo/2)


    #-------------------- window  passenger potato -----------------------------------------

    cg_wdwPot_fb = [cg_cargo_pot_fb[-1]] # front to back
    fb_weight_wdw = [fb_weight_cargo[-1]]

    cg_wdwPot_bf = [cg_cargo_pot_fb[-1]] # back to front
    bf_weight_wdw = [bf_weight_cargo[-1]]
    w_pax = 80 # kg

    #front to back
    for dist in seat_pitch:
        new_xcg = (fb_weight_wdw[-1]*cg_wdwPot_fb[-1] + 2*w_pax*dist)/(2*w_pax + fb_weight_wdw[-1])
        cg_wdwPot_fb.append(new_xcg)
        fb_weight_wdw.append(fb_weight_wdw[-1] + 2*w_pax)

    #back to front
    for dist in np.flip(seat_pitch):
        new_xcg = (bf_weight_wdw[-1]*cg_wdwPot_bf[-1] + 2*w_pax*dist)/(2*w_pax + bf_weight_wdw[-1])
        cg_wdwPot_bf.append(new_xcg)
        bf_weight_wdw.append(bf_weight_wdw[-1] + 2*w_pax)

    #---------------------------- Aisle passenger potato --------------------------------

    cg_aislePot_fb = [cg_wdwPot_fb[-1]] #front to back
    fb_weight_aisle = [fb_weight_wdw[-1]]

    cg_aislePot_bf = [cg_wdwPot_bf[-1]]
    bf_weight_aisle =  [bf_weight_wdw[-1]]
    
    #front to back
    for dist in seat_pitch:
        new_xcg = (fb_weight_aisle[-1]*cg_aislePot_fb[-1] + 2*w_pax*dist)/(2*w_pax + fb_weight_aisle[-1])
        cg_aislePot_fb.append(new_xcg)
        fb_weight_aisle.append(fb_weight_aisle[-1] + 2*w_pax)

    #back to front
    for dist in np.flip(seat_pitch):
        new_xcg = (bf_weight_aisle[-1]*cg_aislePot_bf[-1] + 2*w_pax*dist)/(2*w_pax + bf_weight_aisle[-1])
        cg_aislePot_bf.append(new_xcg)
        bf_weight_aisle.append(bf_weight_aisle[-1] + 2*w_pax)

    #--------------------------- Plotting ---------------------------------------------------

    

    # plotting cargo
    plt.plot(vec_convert_lemac(cg_cargo_pot_fb), fb_weight_cargo, ".-", markersize= 12, label= "Cargo FB")
    plt.plot(vec_convert_lemac(cg_cargo_pot_bf), bf_weight_cargo, ".-",markersize= 12,label = "Cargo BF")
    
    #plotting window seats
    plt.plot(vec_convert_lemac(cg_wdwPot_bf), bf_weight_wdw, ".-",label="Window back to front")
    plt.plot(vec_convert_lemac(cg_wdwPot_fb), fb_weight_wdw, ".-", label="Window front to back ")

    #plotting aisle seats
    plt.plot(vec_convert_lemac(cg_aislePot_bf), bf_weight_aisle, ".-",label="Aisle back to front")
    plt.plot(vec_convert_lemac(cg_aislePot_fb), fb_weight_aisle, ".-", label="Aisle front to back ")



    plt.legend()
    plt.show()


loading_diagrams()