import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'Times New Roman'
rcParams['font.size'] = 14
rcParams['axes.labelsize'] = 14
rcParams['axes.titlesize'] = 16
rcParams['legend.fontsize'] = 12

# List of files
files = [
    "Elevated_Tank/100kL/LRB/Data/100kL With LRB Pushover.csv",
    "Elevated_Tank/100kL/LRB/Data/100kL Without LRB Pushover.csv"
]

plt.figure()

for file in files:
    df = pd.read_csv(file)
    # Remove .csv extension for the label
    label = os.path.basename(file).replace(".csv", "").replace(" Pushover", "")
    label = label.replace("100kL ", "")
    line = plt.plot(df["Drift (%)"], df["Base Shear (kN)"], label=label)[0]
    color = line.get_color()
    
    # Find max base shear and corresponding drift
    max_idx = df["Base Shear (kN)"].idxmax()
    max_shear = df.loc[max_idx, "Base Shear (kN)"]
    max_drift = df.loc[max_idx, "Drift (%)"]
    
    # Vertical and horizontal lines
    plt.plot([0, max_drift], [max_shear, max_shear], color=color, linestyle=':', linewidth=1.0)
    plt.plot([max_drift, max_drift], [0, max_shear], color=color, linestyle=':', linewidth=1.0)
    
    # Write values near the axes
    plt.text(max_drift, 15, f'{max_drift:.2f}', color=color, ha='center', va='bottom', fontsize=12, 
             bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))
    plt.text(0.05, max_shear + 15, f'{max_shear:.0f}', color=color, ha='left', va='bottom', fontsize=12, 
             bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))

# Performance level vertical lines
performance_levels = [(0.5, "IO"), (1.5, "LS"), (2.5, "CP")]
for drift, label in performance_levels:
    plt.axvline(x=drift, color='brown', linestyle='--', linewidth=1.0)
    plt.text(drift - 0.05, 480, label, ha='right', va='top', fontsize=12, color='black')

plt.xlabel("Drift (%)")
plt.ylabel("Base Shear (kN)")
plt.title("Pushover Curves for 100kL Tank")
plt.legend(loc='lower right')
plt.xlim(0, 2.7)
plt.ylim(0, 600)
plt.grid(True, axis='y', linewidth=0.7, alpha=0.5)
plt.tight_layout()
plt.show()