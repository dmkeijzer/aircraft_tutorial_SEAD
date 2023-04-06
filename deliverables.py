from atr import stab_norm, neutstab_norm, contr_norm, shs_norm, min_norm, max_norm
from atr_mod import stab_mod, neutstab_mod, contr_mod, shs_mod, min_mod, max_mod
import matplotlib.pyplot as plt
import numpy as np

# clear plotting data
plt.clf()

# Plotting modified scissor lines
plt.plot(stab_mod.get_xdata(), stab_mod.get_ydata(), label= "Stability line ATR72-HE")
plt.plot(neutstab_mod.get_xdata(), neutstab_mod.get_ydata(), "-.", color="gray", label= "Neutral Stability line ATR72-HE")
plt.plot(contr_mod.get_xdata(), contr_mod.get_ydata(), label= "Controllabiltiy line ATR72-HE")
plt.vlines([min_mod, max_mod], -0.5,np.max([np.max(stab_mod.get_ydata()), np.max(contr_mod.get_ydata())]), label= "CG range ATR72-HE", lw= 1 )

# Plotting normal  scissor lines
plt.plot(stab_norm.get_xdata(), stab_norm.get_ydata(), label= "Stability line ATR72-600")
plt.plot(neutstab_norm.get_xdata(), neutstab_norm.get_ydata(), "-.", color="k", label= "Neutral Stability line ATR72-600")
plt.plot(contr_norm.get_xdata(), contr_norm.get_ydata(), label= "Controllabiltiy line ATR72-600")
plt.vlines([min_norm, max_norm], -0.5,np.max([np.max(stab_norm.get_ydata()), np.max(contr_norm.get_ydata())]), label= "CG range ATR72-600", lw= 1 , color= "darkgreen")

# Formatting
plt.xlabel(r"$\frac{X_{cg}}{\overline{c}}$ [-]", fontsize= 16)
plt.ylabel(r"$\frac{S_h}{S}$ [-]", fontsize= 16)

plt.grid(alpha=0.8)
plt.legend()
plt.show()




