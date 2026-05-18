from model_bare import *

# --------------------------------------------------------------------------------
# Gravity Analysis 
# --------------------------------------------------------------------------------
if rigidDiaphragm == 1:
    ops.constraints('Transformation')
else:
    ops.constraints('Plain')

ops.numberer('RCM')
ops.system('BandGen')
ops.test('NormDispIncr', 1e-8, 10)
ops.algorithm('ModifiedNewton')
ops.integrator('LoadControl', 1.0)
ops.analysis('Static')

ops.analyze(1)

ops.loadConst('-time', 0.0)  # Set the time to zero an hold the loads constant

ops.reactions()
total_Rz = 0.0
print("\n--- Vertical Reactions after Gravity Analysis ---")

for node in Base_nodes:   
    Rz = ops.nodeReaction(node, 3)  # DOF 3 = Z (vertical)
    total_Rz += Rz
    print(f"  Node {node}: Rz = {Rz/1000:+.4f} kN")

print(f"\n  Total Vertical Reaction = {total_Rz/1000:.4f} kN")

# --------------------------------------------------------------------------------
# Plotting Mode Shapes and Deformed Shape
# --------------------------------------------------------------------------------
def ModeShapesPlot():
    opsv.plot_defo()
    plt.title("Deformed Shape")

    opsv.plot_mode_shape(1)
    plt.title("Mode 1")

    opsv.plot_mode_shape(2)
    plt.title("Mode 2")

    opsv.plot_mode_shape(3)
    plt.title("Mode 3")

    opsv.plot_mode_shape(4)
    plt.title("Mode 4")

    opsv.plot_mode_shape(5)
    plt.title("Mode 5")

    plt.show()

# ModeShapesPlot()