from math import *
import matplotlib.pyplot as plt
import numpy as np

cr = 2.57
ct = 1.59
c_mac = 2.11847
b = 27.05
MTOW = 23000
sweep = 0

W_w = 14.9 * MTOW
W_wh = 1.8 * MTOW
W_wv = 2 * MTOW
W_en = 10.3 * MTOW
W_fus = 24.8 * MTOW
W_lm = 3.5 * MTOW
W_ln = 0.5 * MTOW

W_fusgroup = W_fus + W_lm + W_ln
W_wgroup = W_w + W_wh + W_wv + W_en
taper = ct/cr
y_lemac = (b/6) * ((1 + 2*taper)/taper)
print(y_lemac)
x_lemac = y_lemac * tan(sweep)


