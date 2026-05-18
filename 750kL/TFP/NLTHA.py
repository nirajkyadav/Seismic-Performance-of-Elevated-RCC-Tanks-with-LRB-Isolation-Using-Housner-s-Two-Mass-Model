import csv
import os

# --------------------------------------------------------------
# Ground Motion
# --------------------------------------------------------------

GM_RSN = 334

pga = 0.35

original_pga_data = {
    5676: 0.36297,
    5259: 0.34798,
    4199: 0.29655,
    3282: 0.32222,
    2510: 0.33066,
    2476: 0.36627,
    334:  0.28209
}

original_pga = original_pga_data[GM_RSN]
factor = (pga * 9810) / original_pga # mm/s2 see the calculation in sheets Final Models Output Data          

direction = 1    # 1, 2 in X and Y Direction respectively

print("=====================================================")
if direction == 1:
    print("Time History Analysis in X Direction...")
elif direction == 2:
    print("Time History Analysis in Y Direction...")
else:
    print("ERROR Direction")

GM_input_file = f"/Users/niraj/Downloads/Projects/Project_Geo_Lab/GM/D/RSN_{GM_RSN}.txt"

load_factors = []

# Read and parse the file
with open(GM_input_file, "r") as f:
    lines = f.readlines()

# Extract time step from the line containing "Time Step"
for line in lines:
    if "Time Step" in line:
        dt = float(line.strip().split(":")[1].split()[0])
        break

# Skip lines until you reach the actual data
data_start_index = next(i for i, line in enumerate(lines) if "Time(sec)" in line) + 1

# Read acceleration values
for line in lines[data_start_index:]:
    if line.strip():  # skip empty lines
        parts = line.strip().split()
        if len(parts) >= 2:
            acc = float(parts[1])
            load_factors.append(acc)

tFinal = dt * len(load_factors) # Final time
print(f"RSN: {GM_RSN}, PGA: {pga}, g: {factor}, dt: {dt}, tFinal: {tFinal:.7f}, nPts: {len(load_factors)}")

# --------------------------------------------------------------
# Model
# --------------------------------------------------------------

from Gravity_Analysis import *
print("Gravity Analysis Done.") 

def EigenValues(nModes):
    lambdas = ops.eigen(nModes)  # returns a list of eigenvalues

    omega = []
    frequencies = []
    periods = []

    for lam in lambdas:
        sqrt_lam = lam ** 0.5
        omega.append(sqrt_lam)
        frequencies.append(sqrt_lam / (2 * np.pi))
        periods.append(round(((2 * np.pi) / sqrt_lam),5))
    
    return periods

# --------------------------------------------------------------
# RAYLEIGH damping (D = αM*M + βKcurr*Kcurrent + βKcomm*KlastCommit + βKinit*Kinitial)
# --------------------------------------------------------------

# Get first two structural modes (excluding convective modes)
modes = ops.eigen(6)
omegas = [lam**0.5 for lam in modes]
omega_i = omegas[2]   # first structural mode (≈ 3.53 rad/s)
omega_j = omegas[3]   # second structural mode (≈ same, orthogonal)

# Stiffness-proportional coefficient for 5% damping at omega_i and omega_j
zeta = 0.05
betaK = 2 * zeta / (omega_i + omega_j)   # no alphaM

# Define regions
# ops.region(1, '-ele', *all_elements)   # all staging elements
# ops.region(2, '-ele', 1112)            # convective spring

# Apply Rayleigh damping with ONLY betaK, restricted to staging region
# ops.rayleigh(0.0, 0.0, betaK, 0.0, '-region', 1)   # alphaM=0, betaKcurr=0, betaKinit=betaK, betaKcomm=0 
ops.rayleigh(0.0, 0.0, betaK, 0.0, '-ele', *all_elements)

# --------------------------------------------------------------
# Analysis by floor
# --------------------------------------------------------------

ops.wipeAnalysis()

ops.timeSeries('Path', 200, '-dt', dt, '-values', *load_factors, '-factor', factor)   # tag = 200
ops.pattern('UniformExcitation',  200,   direction,  '-accel', 200) 

ops.constraints('Transformation')
# ops.test('NormDispIncr', 1.0e-6, 50)
ops.test('EnergyIncr', 5.0e-4,  50 )
ops.algorithm('Newton')
ops.numberer('RCM')
ops.system('BandGen')
ops.integrator('Newmark',  0.5,  0.25 )
ops.analysis('Transient')

# Transient Analysis -----------------------------------------------------
# tFinal = nPts * dt
tCurrent = ops.getTime()
ok = 0

control_node = master_nodes[-1]     # node where displacement is read (Master Node of top floor)
NBayZ = 8
nodes_for_IDR = master_nodes

time = []
baseshear = []
overturning_moment = []                                # Base overturning moment (OTM)
control_node_disp = []
TFP_disp = []
drifts_all_floors = [[] for _ in range(NBayZ)]        # One list per floor
global_drifts = []

# Over Turning Moment DOF: for X-excitation (direction=1) → My = DOF 5
#                          for Y-excitation (direction=2) → Mx = DOF 4
otm_dof = 5 if direction == 1 else 4

floor_accels = {node: [] for node in vertical_nodes}    # Initialize acceleration storage

while ok == 0 and tCurrent < tFinal: 
    ok = ops.analyze(1, dt)

    if ok != 0:
        print("regular newton failed ... trying ModifiedNewton...")
        ops.test('NormDispIncr', 5.0e-4,  100, 0)
        ops.algorithm('ModifiedNewton')
        ok = ops.analyze( 1, 0.0005)
        if ok == 0:
            # print("ModifiedNewton worked .. back to regular newton")
            ops.test('EnergyIncr', 5.0e-4,  50 )
            ops.algorithm('Newton')
        else:
            # print("ModifiedNewton failed ... trying Broyden...")
            ops.algorithm('Broyden')
            ok = ops.analyze( 1, .0001)
        if ok == 0:
            # print("Broyden worked .. back to regular newton")
            ops.algorithm('Newton')
        else:
            # print("Broyden failed ... trying NewtonLineSearch...")
            ops.algorithm('NewtonLineSearch')
            ok = ops.analyze( 1, .0001)
        if ok == 0:
            # print("NewtonLineSearch worked .. back to regular newton")
            ops.algorithm('Newton')
        else:
            # print("NewtonLineSearch failed ... trying KrylovNewton...")
            ops.algorithm('KrylovNewton')
            ok = ops.analyze( 1, .0001)
        if ok == 0:
            # print("KrylovNewton worked .. back to regular newton")
            ops.algorithm('Newton')
        else:
            print('Analysis Not Successful..')

    tCurrent = ops.getTime()
    time.append(tCurrent)
    ops.reactions()
    basereac = sum(ops.nodeReaction(n, direction) for n in Base_nodes)
    baseshear.append(basereac / 1000)

    # Overturning moment: sum of moment reactions (DOF 4 or 5) at base nodes
    otm_reac = sum(ops.nodeReaction(n, otm_dof) for n in Base_nodes)
    overturning_moment.append(otm_reac / 1.0e6)  # Convert N·mm → kN·m

    control_node_disp.append(ops.nodeDisp(control_node, direction))
    TFP_disp.append(ops.nodeDisp(master_nodes[0], direction))

    # Record absolute floor acceleration at each master node
    # nodeAccel() returns relative acceleration; add ground acceleration to get absolute
    ground_acc = load_factors[min(round(tCurrent / dt), len(load_factors) - 1)] * factor  # mm/s²
    for node in vertical_nodes:
        rel_acc = ops.nodeAccel(node, direction)          # relative accel (mm/s²)
        abs_acc = (rel_acc + ground_acc) / g              # convert to g
        floor_accels[node].append(abs_acc)

    top_node_disp = ops.nodeDisp(control_node, direction)

    top_node_drift = abs(top_node_disp) / 28200.0
    global_drifts.append(top_node_drift)

    for temp_floor in range(NBayZ):
        bottom_node = nodes_for_IDR[temp_floor]   
        top_node = nodes_for_IDR[temp_floor + 1]    

        bottom_disp = ops.nodeDisp(bottom_node, direction)
        top_disp = ops.nodeDisp(top_node, direction)

        if temp_floor == 0:
            bay_width_Z = 4000.0
        elif temp_floor == 7:
            bay_width_Z = 3200.0
        else:
            bay_width_Z = 3500.0

        drift = abs(top_disp - bottom_disp) / bay_width_Z
        drifts_all_floors[temp_floor].append(drift)

# Eigenvalue analysis after earthquake -----------------------------------------------------
Final_TimePeriods = EigenValues(3)
print("Final Time Periods: ", [f"{p:.10f}" for p in Final_TimePeriods])

# Maximum Induced Base Shear -----------------------------------------------------
max_base_shear = max(np.abs(baseshear))
print(f"Maximum Induced Base Shear = {max_base_shear:.4f} kN")

# ── Print maximum absolute floor accelerations ──────────────────────────────
print("\n--- Maximum Absolute Floor Accelerations ---")
max_floor_accels = {}
for node in vertical_nodes:
    max_acc = max(np.abs(floor_accels[node]))
    max_floor_accels[node] = max_acc
    print(f"Node {node}: Peak Acceleration = {max_acc:.6f} g")

# Maximum Overturning Moment (OTM) ------------------------------------------------
max_otm = max(np.abs(overturning_moment))
print(f"Maximum Overturning Moment = {max_otm:.4f} kN·m")

max_control_node_disp = max(np.abs(control_node_disp))
max_TFP_disp = max(np.abs(TFP_disp))
print(f"Maximum Top Displacement = {max_control_node_disp:.4f} mm")
print(f"Maximum TFP Displacement = {max_TFP_disp:.4f} mm")

MIDRs = [max(drifts) for drifts in drifts_all_floors]

for i in range(NBayZ):
    print(f'MIDR for Floor {i+1} = {MIDRs[i] * 100:.4f} %')

MIDRall = max(MIDRs)
print(f'MIDR ALL = {MIDRall * 100:.4f} %')

print("Maximum Global Drift = ", max(global_drifts) * 100, "%")

ops.loadConst('-time', 0.0)
ops.remove('recorders') 