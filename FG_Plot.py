import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.lines import Line2D
rcParams['font.family'] = 'Times New Roman'

df = pd.read_csv('/Users/niraj/Downloads/Projects/Project_Geo_Lab/Elevated_Tank/100kL/LRB/Data/Combined 100kL D.csv')

pga = df["PGA (g)"]

columns = {
    "IO With LRB": "With LRB PoE(IO)",
    "IO Without LRB": "Without LRB PoE(IO)",
    
    "LS With LRB": "With LRB PoE(LS)",
    "LS Without LRB": "Without LRB PoE(LS)",
    
    "CP With LRB": "With LRB PoE(CP)",
    "CP Without LRB": "Without LRB PoE(CP)",
}

plt.figure(figsize=(10, 7))

plt.plot(pga, df[columns["IO With LRB"]], color="tab:blue", linewidth=1.75, linestyle=(0, (5, 2)))
plt.plot(pga, df[columns["IO Without LRB"]], color="tab:orange", linewidth=1.75, linestyle=(0, (5, 2)))

plt.plot(pga, df[columns["LS With LRB"]], color="tab:blue", linewidth=1.75, label="With LRB")
plt.plot(pga, df[columns["LS Without LRB"]], color="tab:orange", linewidth=1.75, label="Without LRB")

plt.plot(pga, df[columns["CP With LRB"]], color="tab:blue", linewidth=1.75, linestyle=(0, (3, 1, 1, 1)))
plt.plot(pga, df[columns["CP Without LRB"]], color="tab:orange", linewidth=1.75, linestyle=(0, (3, 1, 1, 1)))

plt.xlabel("PGA (g)", fontsize=15)
plt.ylabel("Probability of Exceedance", fontsize=15)
plt.tick_params(direction='in', right=True, labelsize=15)
plt.title("Fragility Curves for 100 kL Tank on Soil Type D", fontsize=15)
plt.xlim(0, 2)
plt.ylim(0, 1)
plt.grid(True, linewidth=0.7, alpha=0.7)
# Existing handles for retrofit type (color)
handles, labels = plt.gca().get_legend_handles_labels()

# Proxy artists for performance level (line style)
line_type_handles = [
    Line2D([0], [0], color='black', linewidth=1.75, linestyle=(0, (5, 2)), label='IO'),
    Line2D([0], [0], color='black', linewidth=1.75, linestyle='-',  label='LS'),
    Line2D([0], [0], color='black', linewidth=1.75, linestyle=(0, (3, 1, 1, 1)),  label='CP')
]

plt.legend(handles=handles + line_type_handles, fontsize=15)

plt.tight_layout()
plt.show()