
from atr import vec_convert_lemac
import matplotlib.pyplot as plt
from const_mod import *
import latexify

MTOW = 23000

def cg_modification(mtow):

    W_w = 0.149 * mtow*0.80738 # wing computed using assumptions that all weight decrease of wing group is due to the wing
    W_wh = 0.018 * mtow # wing horizontal
    W_wv = 0.02 * mtow # wing vertical
    W_en = 0.103 * mtow # engine
    W_fus = 0.248 * mtow*1.02 # fuselage weight
    W_lm = 0.035 * mtow # main landing gear
    W_ln = 0.005 * mtow # nose landing gear

    W_fusgroup = (W_fus + W_wh + W_wv + W_ln)
    W_wgroup = (W_w  + W_en + W_lm)
    OEW = W_fusgroup + W_wgroup

    cg_w = 12.35
    cg_wh = 26.47
    cg_wv = 24.15
    cg_en = 11.32
    cg_fus = 0.39 * l_tot
    cg_lm = 12.69
    cg_ln = 1.64

    cg_wgroup = (W_w*cg_w + W_lm*cg_lm + W_en*cg_en)/W_wgroup
    cg_fusgroup = (W_fus*cg_fus + W_wh*cg_wh + W_wv*cg_wv + W_ln*cg_ln)/W_fusgroup

    cg_OEW = (cg_wgroup*W_wgroup + cg_fusgroup*W_fusgroup)/(OEW)
     

    front_bat_weight = 400
    back_bat_weight = 800
    PW = 7400

    front_cargo_dist = 2.5922 # meter
    back_cargo_weight = 21.912 # meter

    OEW_mod = OEW + front_bat_weight + back_bat_weight
    cg_OEW_mod = (OEW*cg_OEW + front_cargo_dist*front_cargo_dist + back_bat_weight*back_cargo_weight)/(OEW_mod)
    cg_OEW_mod_lemac =  convert_lemac(cg_OEW_mod)

    return cg_OEW_mod, cg_OEW_mod_lemac, OEW_mod, PW

def loading_diagrams_mod(cg_OEW, OEW, PW, plot= True):
    seat_pitch = np.arange(6, 18.963 - 2*29*0.0254, 29*0.0254)

    front_cargo = 2.5922 # meter
    back_cargo = 21.912 # meter
    cargo_dist = [front_cargo, back_cargo]

    max_cargo = PW - 4*np.size(seat_pitch)*80 # kg
    
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

    # --------------------------- Fuel ---------------------------------------------------
    FW = MTOW - OEW - PW
    cg_fuel = 11.97

    cg_tot = (cg_aislePot_bf[-1]*bf_weight_aisle[-1] + cg_fuel*FW)/MTOW
    cg_tot_array = [cg_aislePot_bf[-1], cg_tot]
    MTOW_array = [bf_weight_aisle[-1], MTOW]



    #--------------------------- Plotting ---------------------------------------------------

    # plotting cargo
    plt.plot(vec_convert_lemac(cg_cargo_pot_fb), fb_weight_cargo, ".-", markersize= 12, label= "Cargo front to back")
    plt.plot(vec_convert_lemac(cg_cargo_pot_bf), bf_weight_cargo, ".-",markersize= 12,label = "Cargo back to front")
    
    #plotting window seats
    plt.plot(vec_convert_lemac(cg_wdwPot_bf), bf_weight_wdw, ".-",label="Window back to front")
    plt.plot(vec_convert_lemac(cg_wdwPot_fb), fb_weight_wdw, ".-", label="Window front to back ")

    #plotting aisle seats
    plt.plot(vec_convert_lemac(cg_aislePot_bf), bf_weight_aisle, ".-",label="Aisle back to front")
    plt.plot(vec_convert_lemac(cg_aislePot_fb), fb_weight_aisle, ".-", label="Aisle front to back ")

    plt.plot(vec_convert_lemac(cg_tot_array), MTOW_array, ".-", label="Fuel weight added ")

    max_cg = max([max(cg_cargo_pot_bf), max(cg_wdwPot_bf), max(cg_aislePot_bf), cg_tot])
    min_cg = min([min(cg_cargo_pot_fb), min(cg_wdwPot_fb), min(cg_aislePot_fb), cg_tot])

    max_cg = convert_lemac(max_cg)
    min_cg = convert_lemac(min_cg)

    print("The most front and aft cg position of the OEW + PW is: ", max_cg, min_cg)
    plt.xlabel('cg location measured from LEMAC as a percentage of MAC')
    plt.ylabel('Weight in [kg]')
    plt.legend(prop={'size': 8})
    if plot:
        plt.show()
    return max_cg, min_cg

def scissor_plot_mod(SM, max_cg, min_cg):
    """
    :param SM: stability margin
    :type SM: float
    """    
    plt.clf()

    xcg_bar = np.linspace(-1,1, 1000)
    sh_s_range = np.linspace(0, 0.4, 1000)

    #stability line creation
    a0 = 1/(CL_ah/CL_a_tailles*(1 - deda)*lh_c*vh_v**2)
    b0 = -(xac_bar - SM)/(CL_ah/CL_a_tailles*(1 - deda)*lh_c*vh_v**2)
    sh_s_stab = a0*xcg_bar + b0
    x0 = (sh_s_range - b0)/a0

    #neutral stability line creation
    a = 1/(CL_ah/CL_a_tailles*(1 - deda)*lh_c*vh_v**2)
    b = -(xac_bar)/(CL_ah/CL_a_tailles*(1 - deda)*lh_c*vh_v**2)
    sh_s_NeutStab = a*xcg_bar + b

    # contralliblity line creation
    a1 = 1/(CL_h_max/CL_tailles_max*lh_c*vh_v**2)
    b1 = (cm_ac/CL_tailles_max- xac_bar)/(CL_h_max/CL_tailles_max*lh_c*vh_v**2)
    sh_s_contr = a1*xcg_bar + b1
    x1 = (sh_s_range - b1)/a1


    # Plotting the actual scissor plot
    plt.plot(xcg_bar, sh_s_stab, color= "k", lw= 2, label="Stability line")
    plt.plot(xcg_bar, sh_s_NeutStab, "-", color= "b", lw= 2, label="Neutral Stability line")
    plt.plot(xcg_bar, sh_s_contr, "-.", color= "k", lw= 2, label="Controllability line ")

    plt.fill_between(xcg_bar, sh_s_NeutStab, color= 'red', alpha= 0.4)
    plt.fill_between(xcg_bar, sh_s_contr, color= 'red', alpha= 0.4)

    # Fitting cg range in plot
    idx1 = np.isclose(x1, min_cg, atol=0.01)
    idx0 = np.isclose(x0, max_cg, atol=0.01)
    if all(np.logical_not(idx1)) or all(np.logical_not(idx0)):
        solution = False
    else:
        solution = True
        sh_s = np.max([np.max(x1[idx1]*a1 + b1),np.max(x0[idx0]*a0 + b0)])



    plt.ylim([0, np.max([np.max(sh_s_stab), np.max(sh_s_contr)])])
    # plt.hlines(sh_s, min_cg, max_cg, colors= "k", lw=4,alpha=0.8, label= "Actual shift from loading diagram")
    if solution:
        plt.hlines(sh_s, min_cg , max_cg, colors="fuchsia", lw = 2, label= "$S_h = $" + str(np.round(sh_s, 4)) + " tail sizing." + "\n" +  r"Actual $\frac{S_h}{S} = $" + str(np.round(s_h/s,4)) )
    plt.vlines([min_cg, max_cg], 0,np.max([np.max(sh_s_stab), np.max(sh_s_contr)]), label= "Min and max CG", lw= 2, colors="darkorange" )
    plt.ylabel(r"$\frac{S_h}{S}$ [-]", fontsize= 16)
    plt.xlabel(r"$\frac{X_{cg}}{\overline{c}}$ [-]", fontsize= 16)
    plt.legend()
    plt.show()



if __name__ == "__main__":
    cg_oew, cg_oew_lemac, OEW, PW=cg_modification(MTOW)
    max, min = loading_diagrams_mod(cg_oew, OEW, PW, plot=True)
    scissor_plot_mod(0.05, max, min )