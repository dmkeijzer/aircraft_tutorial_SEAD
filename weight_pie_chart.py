import matplotlib.pyplot as plt


fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%')