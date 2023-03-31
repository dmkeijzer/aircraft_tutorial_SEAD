import matplotlib.pyplot as plt
from const_pre import *
from scipy.constants import g
import numpy as np

col = ["lightgrey", "cornflowerblue", "peru"]

labels1 = ["Payload Weight", "Fuel Weight", "OEW"]
sizes1 = np.array([7400, 2000 , 13600])*g

labels2 = ["Payload Weight", "Fuel Weight", "OEW"]
sizes2 = np.array([4400, 5000 , 13600])*g

fig, axs = plt.subplots(1,2)

ft = 14

axs[0].set_title("Payload Weight maximized", fontsize= 18)
axs[0].pie(sizes1, labels=labels1, colors= col, autopct='%1.1f%%', textprops={'fontsize': ft})
axs[1].set_title("Fuel Weight Maximized", fontsize= 18)
axs[1].pie(sizes2, labels=labels2, colors= col, autopct='%1.1f%%',  textprops={'fontsize': ft})


plt.show()