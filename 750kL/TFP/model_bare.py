import openseespy.opensees as ops
import numpy as np
import matplotlib.pyplot as plt
import opsvis as opsv

from nodal_mass_and_udl import *

if TFP_inclusion == 1:
    from TFP_elements import *

# --------------------------------------------------------------------------------
# Eigenvalue Analysis 
# --------------------------------------------------------------------------------
numModes = 5
lambdas = ops.eigen(numModes)  # returns a list of eigenvalues
# print(lambdas)

omega = []
frequencies = []
periods = []

for lam in lambdas:
    sqrt_lam = lam ** 0.5
    omega.append(sqrt_lam)
    frequencies.append(sqrt_lam / (2 * np.pi))
    periods.append((2 * np.pi) / sqrt_lam)

print("Initial Time Periods:", [f"{p:.10f}" for p in periods])

UDL_applier()

def Plotter():
    opsv.plot_model(node_labels = 0, element_labels = 0)     # 1 to see, 0 to hide
    plt.title("3D Model")

    # opsv.plot_load(nep=10, sfac= 500, node_supports=True)
    # plt.title("UDL applied")

    # # Format all text labels to 2 decimal places
    # for text in plt.gca().texts:
    #     try:
    #         value = float(text.get_text())
    #         text.set_text(f"{value:.2f}")
    #     except ValueError:
    #         pass  # Skip if not a number

    plt.show()

# Plotter()